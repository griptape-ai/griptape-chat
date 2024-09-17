import os
import time
import gradio as gr
import requests
from dotenv import load_dotenv
from griptape.chat_cloud import ChatAwsCloud
from griptape.chat_cloud import ChatGTCloud
from griptape.chat_local import ChatLocal

# Load the environment variables
load_dotenv()

# Get the port from the environment variables for Gradio (default is 7860)
port = os.getenv("GRADIO_PORT", 7860)

# Get the lambda endpoint from environment variables if using CDK based memory
lambda_endpoint = os.getenv("LAMBDA_ENDPOINT", "")


# Function to get the session id from the lambda endpoint
def get_session_id() -> str:
    resp = requests.post(lambda_endpoint, json={"operation": "create_session"})
    session_id = resp.json()["session_id"]
    return session_id


# Function to get the thread id from the Griptape Cloud API
def get_thread_id(base_url: str, api_key: str) -> str:
    resp = requests.post(
        f"{base_url}/api/threads",
        json={"name": "Griptape Chat Demo Thread"},
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    thread_id = resp.json()["thread_id"]
    return thread_id


def get_title() -> str:
    return "Griptape Chat Demo"


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
    # This means that either:
    # 1. The Structure is making use of Griptape Cloud Threads for Memory
    # 2. The CDK from https://github.com/griptape-ai/griptape-structure-chatbot has been deployed and LAMBDA_ENDPOINT must be defined.
    host = os.environ["GT_CLOUD_BASE_URL"]
    structure_id = os.environ["GT_STRUCTURE_ID"]
    api_key = os.environ["GT_CLOUD_API_KEY"]
    if lambda_endpoint != "":
        chat = ChatAwsCloud(base_url=host, structure_id=structure_id, api_key=api_key)
        demo = gr.ChatInterface(
            fn=chat.send_message,
            title=get_title(),
            additional_inputs=[gr.State(value=get_session_id())],
        )
    else:
        chat = ChatGTCloud(base_url=host, structure_id=structure_id, api_key=api_key)
        demo = gr.ChatInterface(
            fn=chat.send_message,
            title=get_title(),
            additional_inputs=[gr.State(value=get_thread_id(host, api_key))],
        )
else:
    # Launch the chat interface locally.
    # This just runs a simple local agent in chat_local.py.
    # The only environment variable that must be defined is OPENAI_API_KEY.
    chat = ChatLocal()
    demo = gr.ChatInterface(fn=chat.send_message, title=get_title())

demo.launch(share=True)
# Destroy the file path for local conversation memory if used
if os.path.exists("conversation_memory.json"):
    os.remove("conversation_memory.json")
    print("Conversation memory file removed.")
