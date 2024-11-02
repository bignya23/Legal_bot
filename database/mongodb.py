import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from generate_embeddings import generate_embeddings
from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np

load_dotenv()
# Create a new client and connect to the server
client = MongoClient(os.getenv("MONGO_DATABASE_URL"), server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



db = client["legal_bot"]
collection = db["ipc"]

page_contents = generate_embeddings()
model_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

inserted_doc_count = 0
for page_content in page_contents:

    embedding = model_embedding.embed_query(page_content)
    

    collection.insert_one({ "text": page_content, "embedding": embedding})
    inserted_doc_count += 1
    print(f"Inserted {inserted_doc_count} documents.")



print("Data successfully inserted into MongoDB!")

