import os
import time
import gradio as gr
from dotenv import load_dotenv
from griptape.chat_demo import Chat

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

with gr.Blocks() as demo:
    with gr.Row():

        with gr.Column(scale=1):
            gr.Label("Griptape Chat", show_label=False)
            gr.Text(
                "Before using chat, do the following:\n\n1. Make the OpenAI API token available via an environment "
                "variable OPENAI_API_KEY", 
                show_label=False
            )
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(show_label=False)

            msg_textbox = gr.Textbox(placeholder="Send a message", show_label=False)

            msg_textbox.submit(user, [msg_textbox, chatbot], [msg_textbox, chatbot], queue=False).then(
                bot, chatbot, chatbot
            )
            
    demo.queue()
    demo.launch(share=True)
