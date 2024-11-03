import os
import google.generativeai as genai
import dotenv

# Load environment variables
dotenv.load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

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

# Initialize user_input
user_input = ""

while user_input.lower() != "stop":  # Continue until the user types 'stop'
    # Prompt the user for input
    user_input = input("You: ")  # Get user input

    if user_input.lower() != "stop":  # Avoid sending 'stop' to the model
        # Send the user's input to the model
        response = chat_session.send_message(user_input)

        # Print the model's response
        print("Bot:", response.text)
