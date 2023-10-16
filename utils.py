import base64
import io
import json
import os

import requests
from dotenv import load_dotenv
from PIL import Image

load_dotenv()  # Load environment variables from .env file
hf_api_key = os.getenv("HF_API_KEY")  # Huggingface API

# Image to Text API
ITT_ENDPOINT = (
    "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
)
# Text to Image API
TTI_ENDPOINT = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"


def get_request(inputs, task):
    """
    Sent request to Huggingface API and return the response

    Args:
        inputs: text or image in base64
        task: captioner for image to text or generator for text to image

    Returns:
        Caption of input image or output image of genarated caption
    """
    headers = {
        "Authorization": f"Bearer {hf_api_key}",
        "Content-Type": "application/json",
    }

    ENDPOINT_URL = ITT_ENDPOINT if task == "captioner" else TTI_ENDPOINT
    data = {"inputs": inputs}
    response = requests.request(
        "POST", ENDPOINT_URL, headers=headers, data=json.dumps(data)
    )

    try:
        output = json.loads(response.content.decode("utf-8"))
    except UnicodeDecodeError:
        output = response.content

    return output


def image_to_base64_str(pil_image):
    """
    Save input image in PNG format then read to image

    Args:
        pil_image: pil type image which received from gradio interface

    Returns:
        Input image in base64 string form
    """
    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format="PNG")
    byte_arr = byte_arr.getvalue()
    return str(base64.b64encode(byte_arr).decode("utf-8"))


def base64_to_pil(base64_decoded):
    """
    Transform base64 decoded image to pil image

    Args:
        base64_decoded: base64 encoded image

    Returns:
        PIL image
    """
    byte_stream = io.BytesIO(base64_decoded)
    pil_image = Image.open(byte_stream)
    return pil_image


def captioner(image):
    """
    Generate caption from image

    Args:
        image: input image

    Returns:
        Generated text
    """
    base64_image = image_to_base64_str(image)
    result = get_request(base64_image, task="captioner")
    return result[0]["generated_text"]


def generator(caption):
    """
    Transform caption to image

    Args:
        caption: generated caption from the input image

    Returns:
        Generated image
    """
    output = get_request(caption, task="generator")
    result_image = base64_to_pil(output)
    return result_image


def caption_and_generate(image):
    """
    Generate caption from image then re-generate image

    Args:
        image: input image

    Returns:
        Generated text and image
    """
    caption = captioner(image)
    image = generator(caption)
    return [caption, image]
