import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
import time 
from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEmbeddings
# Connect to your Atlas deployment

load_dotenv()
uri = os.getenv("MONGO_DATABASE_URL")
client = MongoClient(uri)

# Access your database and collection
database = client["legal_bot"]
collection = database["ipc"]

model_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#Query for the seach in database
query = "car accident"


# Generate embedding for the search query
query_embedding = model_embedding.embed_query(query)

# Sample vector search pipeline
pipeline = [
   {
      "$vectorSearch": {
            "index": "legal_bot_index",
            "queryVector": query_embedding,
            "path": "embedding",
            "exact": True,
            "limit": 5
      }
   }, 
   {
      "$project": {
         "_id": 0, 
         "text": 1,
         "score": {
            "$meta": "vectorSearchScore"
         }
      }
   }
]

# Execute the search
results = collection.aggregate(pipeline)

# Print results
for i in results:
   print(i)
