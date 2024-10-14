import os
from dotenv import load_dotenv
import google.generativeai as genai
from react_agent import ReActAgent
from tools import duckduckgo_search, wikipedia_search
from google.api_core import exceptions as google_exceptions

# Load environment variables
load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Set up the model
model = genai.GenerativeModel('gemini-pro')

def print_callback(event):
    if event['type'] == 'iteration':
        print(f"\nIteration {event['number']}")
    elif event['type'] == 'message':
        print(f"{event['role'].capitalize()}: {event['content']}")
    elif event['type'] == 'model_response':
        print(f"Model response: {event['content']}")
    elif event['type'] == 'error':
        print(f"Error: {event['content']}")

# Create the ReAct agent
agent = ReActAgent(model, callback=print_callback)

# Register the DuckDuckGo search and Wikipedia tools
agent.register_tool("search", duckduckgo_search)
agent.register_tool("wikipedia", wikipedia_search)

# Main interaction loop
if __name__ == "__main__":
    print("ReAct Agent: Hello! I'm here to help you. What would you like to know?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("ReAct Agent: Goodbye!")
            break
        
        try:
            response = agent.run(user_input)
            print(f"ReAct Agent: {response}")
            print("\n" + "="*50 + "\n")
        except google_exceptions.GoogleAPIError as e:
            print(f"ReAct Agent: I'm sorry, but I encountered an error while processing your request. "
                  f"This might be a temporary issue. Please try again later. Error details: {str(e)}")
        except Exception as e:
            print(f"ReAct Agent: An unexpected error occurred. Please try again. Error details: {str(e)}")
