import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
import time 
from dotenv import load_dotenv
import os
# Connect to your Atlas deployment

load_dotenv()
uri = os.getenv("MONGO_DATABASE_URL")
client = MongoClient(uri)

# Access your database and collection
database = client["legal_bot"]
collection = database["ipc"]

# Create your index model, then create the search index
search_index_model = SearchIndexModel(
  definition={
    "fields": [
      {
        "type": "vector",
        "numDimensions": 384,
        "path": "embedding",
        "similarity": "euclidean"
      },

    ]
  },
  name="legal_bot_index",
  type="vectorSearch",
)

name="legal_bot_index"

result = collection.create_search_index(model=search_index_model)
print("New search index named " + result + " is building.")

# Wait for initial sync to complete
print("Polling to check if the index is ready. This may take up to a minute.")
predicate=None
if predicate is None:
  predicate = lambda index: index.get("queryable") is True

while True:
  indices = list(collection.list_search_indexes(name))
  if len(indices) and predicate(indices[0]):
    break
  time.sleep(5)
print(result + " is ready for querying.")

client.close()
