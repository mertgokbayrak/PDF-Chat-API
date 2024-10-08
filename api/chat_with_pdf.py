import os
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from models.database_setup import database, pdf_metadata
import logging
from logger_config import logger_config

load_dotenv()

logger_config()
logger = logging.getLogger()

# Gemini AI Setup
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

chat_with_pdf_router = APIRouter()


@chat_with_pdf_router.post("/chat/{pdf_id}")
async def chat_with_pdf(pdf_id: str, message: str):
    try:
        logger.info("New chat request", extra={"pdf_id": pdf_id, "message": message})
        query_db = select(pdf_metadata.c.extracted_text).where(pdf_metadata.c.unique_pdf_id == pdf_id)
        result = await database.fetch_one(query_db)

        # Check for the PDF id validity
        if result is None:
            logger.warning("PDF ID not found in database", extra={"pdf_id": pdf_id})
            raise HTTPException(status_code=404, detail="PDF ID not found in database. Please re-enter the PDF ID.")

        pdf_content = result["extracted_text"]
        logger.info("PDF content accessed successfully", extra={"pdf_id": pdf_id})

        # Generating response using Gemini AI
        prompt = (f"For the following PDF content: {pdf_content}, please answer this question: {message}. "
                  f"Provide the response as detailed and clear as possible.")
        response = model.generate_content(prompt)
        logger.info("Response is generated by Gemini AI", extra={"pdf_id": pdf_id,
                                                                 "response_length": len(response.text)})

        return {"response": response.text}

    except Exception as e:
        logger.error("Error occurred during chat request", extra={"pdf_id": pdf_id, "error": str(e)})
        raise HTTPException(status_code=500, detail="Internal Server Error")
