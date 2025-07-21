from fastapi import FastAPI
import gradio as gr
import datetime

from app import MOSApp

app = FastAPI()

@app.get('/')
async def root():
    return 'Gradio app is running at /gradio', 200

current_date = datetime.now().strftime("%Y%m%d")
app = MOSApp(
        dirpath="./samples/data",   # change as you need
        outdir=f"./results/{current_date}",
        progress_dir=f"./progress/{current_date}",
    )
demo = app.create_interface()

app = gr.mount_gradio_app(app, demo, path='/gradio')