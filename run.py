from fastapi import FastAPI
import gradio as gr

from app import MOSApp

app = FastAPI()

@app.get('/')
async def root():
    return 'Gradio app is running at /gradio', 200

demo = MOSApp().create_interface()

app = gr.mount_gradio_app(app, demo, path='/gradio')