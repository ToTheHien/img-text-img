import gradio as gr

from utils import captioner, generator

with gr.Blocks() as demo:
    gr.Markdown("# Image-to-Image")

    # Upload image
    image_upload = gr.Image(label="Your first image", type="pil")

    # Generate caption
    btn_caption = gr.Button("Generate caption")
    caption = gr.Textbox(label="Generated caption")
    btn_caption.click(fn=captioner, inputs=[image_upload], outputs=[caption])

    # Re-generate image
    btn_image = gr.Button("Generate image")
    image_output = gr.Image(label="Generated Image")
    btn_image.click(fn=generator, inputs=[caption], outputs=[image_output])

demo.launch()
