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


def generate_images_from_text(
    prompt: str,
    number_of_images: int = 1,
    aspect_ratio: Optional[str] = None,
    resolution: Optional[str] = None,
):
    """
    Generates images from a text prompt using the Gemini Image Generation Tool.
    """

    client = initialize_gemini()

    print(f"Generating {number_of_images} image(s) with prompt: '{prompt}'...")

    image_config = None

    if aspect_ratio or resolution:

        image_config = genai_types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution,
        )

    config = genai_types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"], image_config=image_config
    )

    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=prompt,
        config=config,
    )

    images = []
    try:
        for part in response.parts:
            if image := part.as_image():
                images.append(image)
    except Exception as e:
        print(f"Error processing API response: {e}")
        for _ in range(number_of_images):
            images.append(Image.new("RGB", (512, 512), "purple"))

    return images


def generate_images_from_images(
    prompt: str,
    input_image_paths: List[str],
    aspect_ratio: Optional[str] = None,
    resolution: Optional[str] = None,
):
    """
    Generates an image using a text prompt and one or more input images.
    """
    client = initialize_gemini()

    content = [prompt]
    for image_path in input_image_paths:
        try:
            input_image = Image.open(image_path)
            content.append(input_image)
        except FileNotFoundError:
            print(f"Error: Input image not found at {image_path}")
            return None

    print(
        f"Generating image with prompt: '{prompt}' and {len(input_image_paths)} input image(s)."
    )

    image_config = None
    if aspect_ratio or resolution:
        image_config = genai_types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution,
        )

    config = genai_types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"], image_config=image_config
    )

    response = client.models.generate_content(
        model=IMAGE_MODEL, contents=content, config=config
    )

    try:
        for part in response.parts:
            if image := part.as_image():
                return [image]  # Return as a list to be consistent
    except Exception as e:
        print(f"Error processing API response: {e}")
        return [Image.new("RGB", (512, 512), "orange")]
