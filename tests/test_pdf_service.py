import pytest
from services.pdf_service import extract_text_from_pdf
from io import BytesIO
from reportlab.pdfgen import canvas


def create_test_pdf():  # Creates a mock pdf
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "This is a test PDF.")
    c.save()
    buffer.seek(0)
    return buffer


def test_extract_text_from_pdf():

    pdf_file = create_test_pdf()
    extracted_text = extract_text_from_pdf(pdf_file)
    assert "This is a test PDF." in extracted_text

