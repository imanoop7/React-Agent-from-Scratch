import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from react_agent import ReActAgent
from tools import duckduckgo_search, wikipedia_search
from google.api_core import exceptions as google_exceptions
import time

# Load environment variables
load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Set up the model
model = genai.GenerativeModel('gemini-pro')

# Streamlit app
st.set_page_config(page_title="ReAct Agent Visualization", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #2b3035;
        color: #ffffff;
    }
    .big-font {
        font-size:20px !important;
        font-weight: bold;
        color: #ffffff;
    }
    .medium-font {
        font-size:16px !important;
        color: #e0e0e0;
    }
    .small-font {
        font-size:14px !important;
        color: #c0c0c0;
    }
    .highlight {
        background-color: #3a3f44;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #3a3f44;
        color: #ffffff;
    }
    .stMarkdown {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 ReAct Agent Visualization")

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = ReActAgent(model, callback=lambda x: st.session_state.events.append(x))
    st.session_state.agent.register_tool("search", duckduckgo_search)
    st.session_state.agent.register_tool("wikipedia", wikipedia_search)
    st.session_state.events = []

# User input
user_input = st.text_input("You:", key="user_input")

if st.button("Send", key="send_button"):
    st.session_state.events = []  # Clear previous events
    try:
        with st.spinner("Agent is thinking..."):
            response = st.session_state.agent.run(user_input)
        st.session_state.events.append({"type": "final_answer", "content": response})
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Display the agent's process
if st.session_state.events:
    st.markdown("## Agent's Thought Process")
    
    for event in st.session_state.events:
        if event['type'] == 'iteration':
            st.markdown(f"### Iteration {event['number']}")
        elif event['type'] == 'message':
            if event['role'] == 'user':
                st.markdown(f"<div class='highlight big-font'>🧑 User: {event['content']}</div>", unsafe_allow_html=True)
            elif event['role'] == 'assistant':
                st.info(f"🤔 Agent thought: {event['content']}")
            elif event['role'] == 'system':
                st.success(f"🔍 Observation: {event['content']}")
        elif event['type'] == 'model_response':
            with st.expander("🧠 Model Response", expanded=False):
                st.code(event['content'], language='json')
        elif event['type'] == 'error':
            st.error(f"❌ Error: {event['content']}")
        elif event['type'] == 'final_answer':
            st.markdown(f"<div class='highlight big-font'>🎉 Final Answer:</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='medium-font'>{event['content']}</div>", unsafe_allow_html=True)
        
        # Add a small delay for a more dynamic feel
        time.sleep(0.5)
        st.empty()

# Display the full conversation history
if st.checkbox("Show full conversation history"):
    st.markdown("## Full Conversation History")
    st.markdown(f"<div class='small-font'>{st.session_state.agent.get_chat_history()}</div>", unsafe_allow_html=True)

# Sidebar with information
st.sidebar.title("About ReAct Agent")
st.sidebar.info(
    "This ReAct Agent uses the Gemini model to reason about queries and take actions using available tools. "
    "It can search the web and Wikipedia to gather information before providing an answer."
)
st.sidebar.markdown("### Available Tools")
st.sidebar.markdown("- 🌐 Web Search")
st.sidebar.markdown("- 📚 Wikipedia")
