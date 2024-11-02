import os
import requests
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
import google.generativeai as genai

load_dotenv()

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_DATABASE_URL"))
database = client["legal_bot"]
collection = database["ipc"]

# Initialize embedding model for queries
model_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load and configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
)

# Start the chat session
chat_session = model.start_chat(history=[])

def retrieve_information(query):
    # Generate embedding for the user query
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

    # Extract the relevant texts from the results
    documents = [result['text'] for result in results]
    return documents

def call_gemini_api(user_input):
    # Send the user's input to the model
    response = chat_session.send_message(user_input)

    # Return the model's response
    return response.text

def chatbot_response(user_input):
    # Retrieve relevant information from the database
    relevant_info = retrieve_information(user_input)

    if relevant_info:
        # Combine the user's input with retrieved information
        full_input = f"{user_input}\nRelevant Information: {' '.join(relevant_info)}"
    else:
        full_input = user_input

    # Call the Gemini API with the combined input
    response = call_gemini_api(full_input)
    return response

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")

client.close()
