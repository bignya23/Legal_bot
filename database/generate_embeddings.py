# %%
import os
import requests
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np


load_dotenv()

def load_pdf(file_path):
    loader = PyPDFDirectoryLoader(file_path)
    documents = loader.load()
    return documents


def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks


def extract_page_contents(extracted_data):
    page_contents = []
        
    for doc in extracted_data:
        page_contents.append(doc.page_content)
        
    return page_contents

def generate_embeddings():


    pdf_path = "./database/pdf"
    print("Files Present" , os.listdir(pdf_path))
    extracted_data = load_pdf(pdf_path)

    print("Extracted_data")


    
    text_chunks = text_split(extracted_data)
    print("Generated text_chunks")

    
    page_contents = extract_page_contents(text_chunks)

    return page_contents
 



if __name__ == "__main__":
    embeddings = generate_embeddings()

