from fastapi.testclient import TestClient
from app import app
from io import BytesIO
from reportlab.pdfgen import canvas

client = TestClient(app)


def create_test_pdf():  # Creates a mock pdf
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "This is a test PDF.")
    c.save()
    buffer.seek(0)
    return buffer


def test_pdf_upload_success():
    pdf_file = create_test_pdf()
    files = {'file': ('test.pdf', pdf_file, 'application/pdf')}

    response = client.post("/v1/pdf", files=files)

    assert response.status_code == 200
    assert "pdf_id" in response.json()


def test_pdf_upload_invalid_file_type():
    files = {'file': ('test.txt', BytesIO(b"text"), 'text/plain')}

    response = client.post("/v1/pdf", files=files)

    assert response.status_code == 400
    assert response.json() == {"detail": "File type must be a pdf. Please try again."}


def test_pdf_upload_file_too_large():
    large_pdf_content = b"0" * (10 * 1024 * 1024 + 1)  # 10MB + 1 byte
    files = {'file': ('large_test.pdf', BytesIO(large_pdf_content), 'application/pdf')}

    response = client.post("/v1/pdf", files=files)

    assert response.status_code == 413
    assert response.json() == {"detail": "File is too large, the max limit is 10 MB. Please try again."}
