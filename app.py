import os
import time
import gradio as gr
import requests
from dotenv import load_dotenv
from griptape.chat_cloud import Chat_Cloud
from griptape.chat_local import Chat_Local
from griptape.chat import Chat

# Load the environment variables
load_dotenv()

# Get the port from the environment variables for Gradio (default is 7860)
port = os.getenv("GRADIO_PORT", 7860)

# Get the lambda endpoint from environment variables if using CDK based memory
# If the lambda endpoint isn't specified, then the structure can ONLY be run LOCALLY.
lambda_endpoint = os.getenv("LAMBDA_ENDPOINT", "")
 
# Function to get the session id from the lambda endpoint (if not running locally).
def get_session_id() -> str:
    resp = requests.post(lambda_endpoint, json={"operation": "create_session"})
    session_id = resp.json()["session_id"]
    return session_id

# Used for the Gradio ChatInterface. 

# Defines the history
def bot(history):
    response = chat.send_message(history[-1][0])
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character

        time.sleep(0.005)

        yield history

# Checks if environment variables are set for the Griptape Cloud or Azure
if "GT_STRUCTURE_ID" in os.environ and os.environ["GT_STRUCTURE_ID"]:
    # Launch the chat interface WITH session state in a managed environment. 
    # This means that the CDK from https://github.com/griptape-ai/griptape-structure-chatbot has been deployed. 
    # LAMBDA_ENDPOINT must be defined. 
    host = os.environ["GT_CLOUD_BASE_URL"]
    structure_id = os.environ["GT_STRUCTURE_ID"]
    api_key = os.environ["GT_CLOUD_API_KEY"]
    chat = Chat_Cloud(base_url=host,structure_id=structure_id,api_key=api_key)
    demo = gr.ChatInterface(fn=chat.send_message, additional_inputs=[gr.State(value=get_session_id())])
else:
    # Launch the chat interface locally WITHOUT Vector Store (Local Agent)
    # This just runs a simple local agent in chat_local.py.
    # The only environment variable that must be defined is OPENAI_API_KEY.  
    chat = Chat_Local()
    demo = gr.ChatInterface(fn=chat.send_message)

demo.launch(share=False)
# Destroy the file path for local conversation memory if used 
if os.path.exists("conversation_memory.json"):
    os.remove("conversation_memory.json")
    print("Conversation memory file removed.")

