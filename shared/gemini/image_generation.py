# shared/image_generation.py
import sys
from pathlib import Path
from PIL import Image
import io
from typing import Optional, List

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from shared.gemini.client import initialize_gemini

IMAGE_MODEL = "gemini-1.5-pro-latest"

def generate_images_from_text(prompt: str, number_of_images: int = 1, aspect_ratio: Optional[str] = None, resolution: Optional[str] = None):
    """
    Generates images from a text prompt using the Gemini Image Generation Tool.
    """
    genai = initialize_gemini()
    
    generation_config = {"response_mime_type": "image/png"}
    image_config = {}
    if aspect_ratio:
        image_config["aspect_ratio"] = aspect_ratio
    if resolution:
        image_config["image_size"] = resolution # Note: API uses 'image_size'
    
    if image_config:
        generation_config["image_config"] = image_config

    model = genai.GenerativeModel(
        IMAGE_MODEL,
        generation_config=generation_config,
    )
    
    print(f"Generating {number_of_images} image(s) with prompt: '{prompt}'...")
    print(f"Config: {generation_config}")
    
    response = model.generate_content(prompt)

    images = []
    try:
        for i in range(number_of_images):
            img_bytes = response.parts[0].data
            image = Image.open(io.BytesIO(img_bytes))
            images.append(image)
    except Exception as e:
        print(f"Error processing API response: {e}")
        for _ in range(number_of_images):
            images.append(Image.new('RGB', (512, 512), 'purple'))
            
    return images

def generate_images_from_images(prompt: str, input_image_paths: List[str], aspect_ratio: Optional[str] = None, resolution: Optional[str] = None):
    """
    Generates an image using a text prompt and one or more input images.
    """
    genai = initialize_gemini()

    generation_config = {"response_mime_type": "image/png"}
    image_config = {}
    if aspect_ratio:
        image_config["aspect_ratio"] = aspect_ratio
    if resolution:
        image_config["image_size"] = resolution

    if image_config:
        generation_config["image_config"] = image_config
        
    model = genai.GenerativeModel(
        IMAGE_MODEL,
        generation_config=generation_config,
    )

    content = [prompt]
    for image_path in input_image_paths:
        try:
            input_image = Image.open(image_path)
            content.append(input_image)
        except FileNotFoundError:
            print(f"Error: Input image not found at {image_path}")
            return None

    print(f"Generating image with prompt: '{prompt}' and {len(input_image_paths)} input image(s).")
    print(f"Config: {generation_config}")
    
    response = model.generate_content(content)
    
    try:
        img_bytes = response.parts[0].data
        image = Image.open(io.BytesIO(img_bytes))
        return [image] # Return as a list to be consistent
    except Exception as e:
        print(f"Error processing API response: {e}")
        return [Image.new('RGB', (512, 512), 'orange')]