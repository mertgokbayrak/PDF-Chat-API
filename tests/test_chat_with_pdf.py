import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from io import BytesIO
from reportlab.pdfgen import canvas
from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database, drop_database
from models.database_setup import metadata, pdf_metadata, database
from app import app

client = TestClient(app)

DATABASE_URL = "sqlite:///./test.db"

def setup_module(module):
    # Create a new test database
    if database_exists(DATABASE_URL):
        drop_database(DATABASE_URL)
    create_database(DATABASE_URL)

    engine = create_engine(DATABASE_URL)
    metadata.create_all(engine)

    # Connect the database for use in the app
    database.url = DATABASE_URL
    database.connect()

def teardown_module(module):
    # Drop the test database after tests
    database.disconnect()
    drop_database(DATABASE_URL)

def create_test_pdf():
    # Create a PDF in memory
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "This is a test PDF.")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def insert_test_pdf_into_db():
    pdf_id = str(uuid4())
    pdf_file = create_test_pdf().read()
    extracted_text = pdf_file.decode("latin1")

    # Insert test PDF data into the database
    query = pdf_metadata.insert().values(
        unique_pdf_id=pdf_id,
        filename="test.pdf",
        extracted_text=extracted_text,
        metadata={"page_count": 1}
    )
    database.execute(query)

    return pdf_id

@pytest.fixture(scope="module")
def test_pdf_id():
    # Insert a PDF into the test database and return its UUID
    return insert_test_pdf_into_db()

def test_chat_with_pdf_success(test_pdf_id):
    response = client.post(f"/v1/chat/{test_pdf_id}", json={"message": "What is the content about?"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_chat_with_pdf_not_found():
    non_existent_pdf_id = str(uuid4())
    response = client.post(f"/v1/chat/{non_existent_pdf_id}", json={"message": "What is the content about?"})
    assert response.status_code == 404


