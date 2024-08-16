import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import pyttsx3

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini Pro model and start chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo", layout="wide")

# Apply dark theme styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: white;
    }
    .css-18e3th9 {
        background-color: #000000; /* Background of the top part */
        color: white;
    }
    .stTextInput input {
        background-color: #333;
        color: white;
    }
    .stButton button {
        background-color: #444;
        color: white;
    }
    .stMarkdown {
        color: white;
    }
    .chat-message {
        background-color: #333;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
    }
    .chat-message-user {
        color: #dcdcdc;
        text-align: right;
    }
    .chat-message-bot {
        color: #ffffff;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("Input: ", key="input", placeholder="Type your question here...")
submit = st.button("Ask the question")

# Show loading spinner while processing
if submit and input_text:
    with st.spinner("Processing..."):
        response = get_gemini_response(input_text)
        response_text = ""
        for chunk in response:
            response_text += chunk.text + "\n"
        
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader("The Response is")
        st.write(response_text)
        st.session_state['chat_history'].append(("Bot", response_text))
        speak(response_text)  # Add text-to-speech feature

st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    if role == "You":
        st.markdown(f"<div class='chat-message chat-message-user'>{role}: {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-message chat-message-bot'>{role}: {text}</div>", unsafe_allow_html=True)
