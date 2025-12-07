# shared/image_generation.py
import sys
from pathlib import Path
from PIL import Image
import io
from typing import Optional, List

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from google.genai import types as genai_types
from shared.gemini.client import initialize_gemini

IMAGE_MODEL = "gemini-3-pro-image-preview"

def _build_image_config(aspect_ratio: Optional[str], resolution: Optional[str]) -> genai_types.GenerateContentConfig:
    """Builds the generation config for an image generation call."""
    image_config = None
    if aspect_ratio or resolution:
        image_config = genai_types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution,
        )
    return genai_types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"], image_config=image_config
    )

def _process_image_response(response, number_of_images: int) -> List[Image.Image]:
    """Processes the response from the Gemini API and extracts images."""
    images = []
    try:
        for part in response.parts:
            if image := part.as_image():
                images.append(image)
    except Exception as e:
        print(f"Error processing API response: {e}")
        # Create fallback images
        for _ in range(number_of_images):
            images.append(Image.new("RGB", (512, 512), "purple"))
    return images

def generate_images_from_text(prompt: str, number_of_images: int = 1, aspect_ratio: Optional[str] = None, resolution: Optional[str] = None) -> List[Image.Image]:
    """Generates images from a text prompt."""
    client = initialize_gemini()
    print(f"Generating {number_of_images} image(s) with prompt: '{prompt}'...")
    config = _build_image_config(aspect_ratio, resolution)
    response = client.models.generate_content(
        model=IMAGE_MODEL, contents=prompt, config=config
    )
    return _process_image_response(response, number_of_images)

async def generate_images_from_text_async(prompt: str, number_of_images: int = 1, aspect_ratio: Optional[str] = None, resolution: Optional[str] = None) -> List[Image.Image]:
    """Asynchronously generates images from a text prompt."""
    client = initialize_gemini()
    print(f"Generating {number_of_images} image(s) with prompt: '{prompt}'...")
    config = _build_image_config(aspect_ratio, resolution)
    response = await client.aio.models.generate_content(
        model=IMAGE_MODEL, contents=prompt, config=config
    )
    return _process_image_response(response, number_of_images)

def generate_images_from_images(prompt: str, input_image_paths: List[str], aspect_ratio: Optional[str] = None, resolution: Optional[str] = None) -> Optional[List[Image.Image]]:
    """Generates an image using a text prompt and one or more input images."""
    client = initialize_gemini()
    content = [prompt]
    for image_path in input_image_paths:
        try:
            input_image = Image.open(image_path)
            content.append(input_image)
        except FileNotFoundError:
            print(f"Error: Input image not found at {image_path}")
            return None
            
    print(f"Generating image with prompt: '{prompt}' and {len(input_image_paths)} input image(s).")
    config = _build_image_config(aspect_ratio, resolution)
    response = client.models.generate_content(
        model=IMAGE_MODEL, contents=content, config=config
    )
    return _process_image_response(response, 1)

async def generate_images_from_images_async(prompt: str, input_image_paths: List[str], aspect_ratio: Optional[str] = None, resolution: Optional[str] = None) -> Optional[List[Image.Image]]:
    """Asynchronously generates an image using a text prompt and input images."""
    client = initialize_gemini()
    content = [prompt]
    for image_path in input_image_paths:
        try:
            input_image = Image.open(image_path)
            content.append(input_image)
        except FileNotFoundError:
            print(f"Error: Input image not found at {image_path}")
            return None

    print(f"Generating image with prompt: '{prompt}' and {len(input_image_paths)} input image(s).")
    config = _build_image_config(aspect_ratio, resolution)
    response = await client.aio.models.generate_content(
        model=IMAGE_MODEL, contents=content, config=config
    )
    return _process_image_response(response, 1)
