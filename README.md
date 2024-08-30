# **PDF Chat API**

## **Overview**

The PDF Chat API is a FastAPI-based application that allows users to upload PDFs, extract text content from them, and interact with the content via a chatbot powered by Gemini AI. The API supports uploading PDFs, querying the content, and receiving detailed responses based on the extracted text. This project is particularly useful for scenarios where users need to query large documents and get specific answers without manually searching through the content.

## Features

* Upload PDFs and store their content in a database.
* Query the PDF content using natural language queries.
* Receive detailed responses generated by Gemini AI based on the PDF content.
* Comprehensive logging and error handling.

## Setup Instructions 

### Prerequisites

Ensure you have the following installed on your machine:

* Python 3.8+
* pip package manager
* SQLite (for local development)

### Environment Configuration

1. Clone the Repository: \
`git clone https://github.com/yourusername/pdf-chatbot-api.git` \
`cd pdf-chatbot-api`


2. Create a Virtual Environment: \
`python3 -m venv venv` \
`source venv/bin/activate` (On Windows use `venv\Scripts\activate`)


3. Install Dependencies:\
`pip install -r requirements.txt`


4. Environment Variables: \
Create a .env file in the root of your project and add the following variables:

`GEMINI_API_KEY=your-gemini-api-key`


### Database Setup

The project uses SQLite for the database. The database will automatically be created and initialized when you first run the application.

## Running the Application

To start the application, use the following command:


`uvicorn app:app --reload` \

This will start the FastAPI server locally on http://localhost:8000.

## API Endpoints

### 1. Upload PDF

**Endpoint:** /v1/pdf\
**Method:** POST\
**Description:** Endpoint for uploading and registering a PDF.\
**Request:**
File: Multipart form data containing the PDF file\
**Response:**
* 200 OK: Returns the unique PDF ID in form of: \
    `{"pdf_id": "unique_pdf_identifier"}`
* 400 Bad Request: Invalid file type or size exceeds limit.
* 413 Payload Too Large: PDF file's size exceeds 10 MB.
* 500 Internal Server Error: Error processing the request.

**Example:**\
`curl -X POST "http://localhost:8000/v1/pdf" -F "file=@/path/to/your/file.pdf"`

### 2. Chat with PDF

**Endpoint:** /v1/chat/{pdf_id} \
**Method:** POST \
**Description:** Endpoint for interacting with a specific PDF. \
**Request:** 
* Path Parameter: _pdf_id_  (UUID of the uploaded PDF)
* Body: { "message": "Your message" }

Response:
* 200 OK: Returns the response from the AI.
* 404 Not Found: PDF ID not found.
* 500 Internal Server Error: Error processing the request.

Example:

`curl -X POST "http://localhost:8000/v1/chat/{pdf_id}" -H "Content-Type: application/json" -d '{"message": "What is the content about?"}'`

## Testing Procedures

### Running the Test Suite

This project includes unit tests and integration tests to ensure the functionality of the API endpoints.

Run Tests:
`pytest`

### Test Coverage:

To check the test coverage, use:
`pytest --cov=.`

### Test Configuration

The tests use an in-memory SQLite database for isolation and speed.
The tests are configured to automatically create and tear down the database.


