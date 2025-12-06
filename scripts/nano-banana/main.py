# scripts/nano-banana/main.py
import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from shared.gemini.image_generation import generate_images_from_text, generate_images_from_images
from utils.image_converter import ensure_png

def main():
    parser = argparse.ArgumentParser(description="Generate images with Gemini.")
    parser.add_argument("prompt", type=str, help="The text prompt for image generation.")
    parser.add_argument("--num-images", type=int, default=1, help="Number of images to generate (for text-to-image).")
    parser.add_argument("--aspect-ratio", type=str, help="Aspect ratio (e.g., '1:1', '16:9').")
    parser.add_argument("--resolution", type=str, help="Output resolution (e.g., '1K', '2K', '4K').")
    parser.add_argument("--input-images", type=str, nargs='+', help="Path to one or more input images for image-to-image generation.")
    parser.add_argument("--output-file", type=str, default="generated_image", help="Base name for the output image file(s).")
    args = parser.parse_args()

    images = []
    if args.input_images:
        # Ensure all input images are in a supported format (PNG)
        processed_image_paths = [ensure_png(p) for p in args.input_images]
        images = generate_images_from_images(
            prompt=args.prompt,
            input_image_paths=processed_image_paths,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution
        )
    else:
        images = generate_images_from_text(
            prompt=args.prompt,
            number_of_images=args.num_images,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution
        )

    if images:
        output_dir = Path(__file__).parent / "images" / "outputs"
        for i, img in enumerate(images):
            base_filename = args.output_file
            # ensure the filename ends with .png
            if not base_filename.lower().endswith('.png'):
                base_filename += '.png'
            
            if len(images) > 1:
                # Insert index before the extension, e.g., image_0.png
                p = Path(base_filename)
                output_filename = f"{p.stem}_{i}{p.suffix}"
            else:
                output_filename = base_filename
                
            output_path = output_dir / output_filename
            img.save(output_path)
            print(f"Image saved as {output_path}")

if __name__ == "__main__":
    main()
