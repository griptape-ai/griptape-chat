import os
import time
import gradio as gr
from dotenv import load_dotenv
from griptape.chat_demo import Chat

#for somereason the program is picky about the names of the files that it takes in, wouldn't take in "Edipo Rey-(bunch of letters and numbers from Anna's archive)-Anna's Archive" but would take the rename "Edipo Rey"?

load_dotenv()
port = os.getenv("GRADIO_PORT", 7860)
chat = Chat()

def user(user_message, history):
    return "", history + [[user_message, None]]

def bot(history):
    response = chat.send_message(history[-1][0])
    history[-1][1] = ""

    for character in response:
        history[-1][1] += character

        time.sleep(0.005)

        yield history

demo = gr.ChatInterface(fn=chat.send_message, examples=["What did EDB release in Q2", "Why is Postgres better than Aurora"], title="Knowledge Base Search Bot")

demo.launch(share=True)
