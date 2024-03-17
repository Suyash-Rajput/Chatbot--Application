from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any,Union
from fastapi import FastAPI, Request, Query, UploadFile, File, Form
import result as result_class
import os, csv
from docx import Document

from PyPDF2 import PdfReader
# Load environment variables from .env file (if any)
load_dotenv()

class Response(BaseModel):
    result: Union[str, None]

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_txt_file(text_file):
    return text_file.file.read()

def read_csv_file(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

def get_pdf_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file.file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_docs_text(docs_file):
    text = ""
    with docs_file.file as f:
        doc_content = f.read()
        from io import BytesIO
        doc_bytes_io = BytesIO(doc_content)
        doc = Document(doc_bytes_io)
        for paragraph in doc.paragraphs:
            text += paragraph.text
    return text


def get_text(fileType, file): 
    pages = ""
    if fileType == "text/csv":
        pages = read_txt_file(file)   
    elif fileType == "application/pdf":
        pages = get_pdf_text(file)
    elif fileType == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        pages = get_docs_text(file)
    elif fileType == "text/plain":
        pages = read_txt_file(file)
    return pages

@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...), question: str = Form(...), fileType: str = Form(...)):
    print("fileType --------", fileType)
    # save_file_to_database(file.filename, file, fileType)
    pages = get_text(fileType, file)
    # raw_text = get_pdf_text(file)
    print("raw_text --------", pages)
    resp = result_class.get_result(pages, question)
    # Access the question
    print("Question:", question)
    # Return appropriate response
    return {"result": resp['output_text']}
