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

prompt_template = """Answer the question as precise as possible using the provided context.\n\n
                    Context: \n {context}?\n
                    Question: \n {question} \n
                    Answer:
                  """
                  
def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000)
    chunks = splitter.split_text(str(text))
    return chunks  # list of strings

def get_result(pages, query):
        chunks = get_text_chunks(pages)
        print("chunks ----------", chunks)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)
        VectorStore = Chroma.from_texts(chunks, embeddings).as_retriever()
        if query:
            print(" query --- ", query)
            docs = VectorStore.get_relevant_documents(query)
            print("Docs:-     --------------  ", docs)
            llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, google_api_key=API_KEY)
            prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
            chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=prompt)
            try:
              response = chain({"input_documents": docs, "question": query}, return_only_outputs=True)
            except Exception as e:
              print(f"An error occurred: {e}")
              return "LLM API is in trouble. Please try again."
            print(response)
            return response
        return "None"
