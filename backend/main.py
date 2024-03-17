from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any,Union
from fastapi import FastAPI, Request, Query, UploadFile, File, Form
import result as result_class
import os
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
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

def get_text(fileType, file): 
    pages = ""
    if fileType == "text/csv":
        path ="E:/llm-assignment-master/backend/temp.csv"
        with open(path, "wb") as buffer:
            buffer.write(file.file.read())
        csv_loader = CSVLoader("E:/llm-assignment-master/backend/temp.csv") 
        pages = csv_loader.load_and_split()   
    elif fileType == "application/pdf":
        path = "E:/llm-assignment-master/backend/temp.pdf"
        with open(path, "wb") as buffer:
            buffer.write(file.file.read())
        pdf_loader = PyPDFLoader("E:/llm-assignment-master/backend/temp.pdf")  
        pages = pdf_loader.load_and_split()
    elif fileType == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        path =  "E:/llm-assignment-master/backend/temp.docs"
        with open(path, "wb") as buffer:
            buffer.write(file.file.read())
        docs_loader = Docx2txtLoader("E:/llm-assignment-master/backend/temp.docs")
        pages = docs_loader.load_and_split()
    elif fileType == "text/plain":
        path = "E:/llm-assignment-master/backend/temp.txt"
        with open(path, "wb") as buffer:
            buffer.write(file.file.read())
        text_loader = TextLoader(path)  
        pages = text_loader.load_and_split()
    return pages

@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...), question: str = Form(...), fileType: str = Form(...)):
    print("fileType --------", fileType)
    pages = get_text(fileType, file)
    resp = result_class.get_result(pages, question)
    # Access the question
    print("Question:", question)
    # Return appropriate response
    return {"result": resp['output_text']}
