import os
import time
import gradio as gr
import requests
from dotenv import load_dotenv
from uuid import uuid4 as uuid
#from griptape.chat_demo import Chat
from griptape.chat_cloud import Chat_Cloud, Chat_Local

#for somereason the program is picky about the names of the files that it takes in, wouldn't take in "Edipo Rey-(bunch of letters and numbers from Anna's archive)-Anna's Archive" but would take the rename "Edipo Rey"?

# Load the environment variables
load_dotenv()

# Get the port from the environment variables for Gradio
port = os.getenv("GRADIO_PORT", 7860)

lambda_endpoint = os.getenv("LAMBDA_ENDPOINT")
 
def get_state():
    resp = requests.post(lambda_endpoint, json={"operation": "create_session"})
    session_id = resp.json()["session_id"]
    return session_id

# Chat from the chat.py file created in the griptape/chat_demo folder (CJ's chatbot)
#chat = Chat()

# Chat from the chat_cloud.py file created in the griptape/chat_cloud folder for cloud and Skatepark
chat = Chat_Cloud()

# Chat from the chat_cloud.py file created in the griptape/chat_cloud folder for local agent
#chat = Chat_Local()


def user(user_message, history):
    return "", history + [[user_message, None]]

def bot(history):
    response = chat.send_message(history[-1][0])
    #response = send_message(history[-1][0])
    history[-1][1] = ""

    for character in response:
        history[-1][1] += character

        time.sleep(0.005)

        yield history

#demo = gr.ChatInterface(fn=chat.send_message, examples=["What did EDB release in Q2", "Why is Postgres better than Aurora"], title="Knowledge Base Search Bot")

# Launch the chat interface with session state
demo = gr.ChatInterface(fn=chat.send_message, additional_inputs=[gr.State(value=get_state())])

# Launch the chat interface without session state
#demo = gr.ChatInterface(fn=chat.send_message)
demo.launch(share=True)

# Destroy the file path for local conversation memory
if os.path.exists("conversation_memory.json"):
    os.remove("conversation_memory.json")
    print("Conversation memory file removed.")

