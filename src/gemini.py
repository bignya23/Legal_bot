import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()


os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-002",
    temperature=0,
    max_tokens=8192,
    timeout=None,
    max_retries=2,
    top_k= 40,
    top_p= 0.95
)

prompt = ChatPromptTemplate.from_template(
"""
Give sarcastic answers to every question I ask:

 {input}

"""
    
)
chain = prompt | llm
user_input = ""

while user_input != "stop":
    user_input = input("You : ")
    output = chain.invoke(
        {
            "input": {user_input},
        }
    )

    print(output.content)


