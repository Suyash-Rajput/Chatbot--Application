from dotenv import load_dotenv
from langchain import PromptTemplate
import numpy as np
import pickle,os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma, FAISS, DocArrayInMemorySearch
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings

load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

prompt_template = """
  Answer the question as detailed as possible from the provided context, make sure to provide all the details,
  Context:\n {context}?\n
  Question: \n{question}\n

  Answer:
"""

def  get_result(text, query):
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
            )
    chunks = text_splitter.split_text(text=text)
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key =  API_KEY)   
    VectorStore = Chroma.from_texts(text, embeddings).as_retriever()
    if query:
            docs = VectorStore.get_relevant_documents(query)
            llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, google_api_key=API_KEY)
            prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
            chain = load_qa_chain(llm =llm, chain_type="stuff", prompt=prompt)
            response = chain({"input_documents":docs, "question": query} , return_only_outputs=True)
            return response
    return "None"