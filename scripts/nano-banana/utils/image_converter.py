# scripts/nano-banana/utils/image_converter.py
import os
from pathlib import Path
from PIL import Image
import pillow_heif

def ensure_png(image_path: str) -> str:
    """
    Ensures an image is available as a PNG.

    If the input is a HEIC file, this function checks if a corresponding PNG
    version already exists. If not, it converts the HEIC file to PNG and saves
    it in the same directory.

    Args:
        image_path: The path to the image file.

    Returns:
        The path to the PNG version of the image, or the original path if
        the input was not a HEIC file.
    """
    path = Path(image_path)

    if path.suffix.lower() == ".heic":
        png_path = path.with_suffix(".png")

        if png_path.exists():
            print(f"Using existing PNG: {png_path}")
            return str(png_path)
        else:
            print(f"Converting HEIC to PNG: {path}")
            try:
                heif_file = pillow_heif.read_heif(path)
                image = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                )
                image.save(png_path, "PNG")
                print(f"Saved new PNG: {png_path}")
                return str(png_path)
            except Exception as e:
                print(f"Error converting HEIC file {path}: {e}")
                # Return original path and let the next step handle the error
                return str(path)
    
    # If not HEIC, return the original path
    return image_path
