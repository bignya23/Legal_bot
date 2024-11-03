import os
import requests
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
# MongoDB Connection
client = MongoClient(os.getenv("MONGO_DATABASE_URL"))
database = client["legal_bot"]
collection = database["ipc"]

# Initialize embedding model for queries
model_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")



llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-002",
    temperature=0,
    max_tokens=8192,
    timeout=None,
    max_retries=2,
    top_k= 40,
    top_p= 0.95
)

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


def chatbot_response(user_input):
    # Retrieve relevant information from the database
    relevant_info = retrieve_information(user_input)
    prompt = ChatPromptTemplate.from_template(
    """
    Based on the user’s query, format the response with a friendly tone and clear structure. 
    Include the most relevant information from the vector database:

    **User Query**: {user_input}

    **Response Structure**:
    - **Introduction**: Start with a brief overview.
    - **Main Content**: Summarize or elaborate on relevant content.
    - **Key Points**: Use bullet points or numbered lists for clarity.
    - **Conclusion**: End with a short wrap-up or additional helpful advice.

    **Relevant Information from Database**:
    {relevant_info}
    use appropriate formatting whereever necessary
    """
    )

    chain = prompt | llm 
    if relevant_info:
        # Combine the user's input with retrieved information
        full_input = f"{user_input}\nRelevant Information: {' '.join(relevant_info)}"
    else:
        full_input = user_input

    output = chain.invoke(
        {
            "user_input": {user_input},
            "relevant_info" : {full_input}
        }
    )
    return output.content

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")




