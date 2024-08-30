from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.pdf_upload import pdf_upload_router
from api.chat_with_pdf import chat_with_pdf_router
from models.database_setup import database
from logger_config import logger_config
import logging

logger_config()
logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Application started, connecting to the database")
        await database.connect()
        yield
    finally:
        logger.info("Application is closed, disconnecting from the database")
        await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(pdf_upload_router, prefix="/v1")
app.include_router(chat_with_pdf_router, prefix="/v1")


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the server")
    uvicorn.run(app, host="localhost", port=8000)
