
import streamlit as st
from src.Chatbot import chatbot_response  # Import the chatbot_response function

st.title("Legal-Bot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user prompt
if prompt := st.chat_input("Ask a legal question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display assistant's response
    with st.chat_message("assistant"):
        response = chatbot_response(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
