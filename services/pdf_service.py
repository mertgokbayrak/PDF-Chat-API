from PyPDF2 import PdfReader
import logging

logger = logging.getLogger()


def extract_text_from_pdf(file):
    try:
        logger.info(f"Extracting text from {file}")
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        logger.info("Text extraction completed.")
        return text
    except Exception as e:
        logger.error(f"Text could not be extracted: {str(e)}")
        raise ValueError("Failed to extract text.")
