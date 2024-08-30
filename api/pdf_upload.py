from fastapi import APIRouter, File, UploadFile, HTTPException
from uuid import uuid4
from services.pdf_service import extract_text_from_pdf
from models.database_setup import database, pdf_metadata
from logger_config import logger_config
import logging

logger_config()
logger = logging.getLogger()

pdf_upload_router = APIRouter()

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # Setting maximum PDF size to 10 MB


@pdf_upload_router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        logging.error(f"Incorrect file type.", extra={"file_type": file.content_type})
        raise HTTPException(status_code=400, detail="File type must be a pdf. Please try again.")

    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE:
        logging.error(f"PDF too large", extra={"file_size": len(content)})
        raise HTTPException(status_code=413, detail="File is too large, the max limit is 10 MB. Please try again.")

    logger.info("File upload successful.", extra={"file_name": file.filename, "file_size": len(content)})

    unique_pdf_id = str(uuid4())  # Generating a random ID for the PDF

    try:
        text = extract_text_from_pdf(file.file)
        logger.info("Text extracted successfully", extra={"pdf_id": unique_pdf_id})
    except Exception as e:
        logger.error("Text could not be extracted", extra={"pdf_id": unique_pdf_id, "error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to extract text from PDF. Please try again.")

    # Store metadata and extracted text in the database
    try:
        query = pdf_metadata.insert().values(
            unique_pdf_id=unique_pdf_id,
            filename=file.filename,
            extracted_text=text,
            page_count=len(text.split("\f"))
        )
        await database.execute(query)
        logger.info("PDF metadata stored.", extra={"pdf_id": unique_pdf_id})
    except Exception as e:
        logger.error("Storage failed", extra={"pdf_id": unique_pdf_id, "error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to store PDF data. Please try again.")

    return {"pdf_id": unique_pdf_id}
