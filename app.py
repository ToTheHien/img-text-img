import gradio as gr

from utils import caption_and_generate

with gr.Blocks() as demo:
    gr.Markdown("# Image-to-Image")

    # Upload image
    image_upload = gr.Image(label="Your first image", type="pil")
    btn_all = gr.Button("Caption and generate")
    caption = gr.Textbox(label="Generated caption")
    image_output = gr.Image(label="Generated Image")

    btn_all.click(
        fn=caption_and_generate, inputs=[image_upload], outputs=[caption, image_output]
    )

demo.launch()
