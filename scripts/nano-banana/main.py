# scripts/nano-banana/main.py
import argparse
import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from shared.gemini.image_generation import generate_images_from_text_async, generate_images_from_images_async
from shared.gemini.text_generation import generate_text_async
from utils.image_converter import ensure_png

async def main():
    parser = argparse.ArgumentParser(description="Generate images with Gemini.")
    parser.add_argument("prompt", type=str, help="The text prompt for image generation.")
    parser.add_argument("--num-images", type=int, default=1, help="Number of images to generate (for text-to-image).")
    parser.add_argument("--aspect-ratio", type=str, help="Aspect ratio (e.g., '1:1', '16:9').")
    parser.add_argument("--resolution", type=str, help="Output resolution (e.g., '1K', '2K', '4K').")
    parser.add_argument("--input-images", type=str, nargs='+', help="Path to one or more input images for image-to-image generation.")
    parser.add_argument("--output-file", type=str, help="Base name for the output image file(s). If not provided, a name will be generated from the prompt.")
    args = parser.parse_args()

    tasks = []
    # Create the image generation task
    if args.input_images:
        processed_image_paths = [ensure_png(p) for p in args.input_images]
        image_task = asyncio.create_task(generate_images_from_images_async(
            prompt=args.prompt,
            input_image_paths=processed_image_paths,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution
        ))
    else:
        image_task = asyncio.create_task(generate_images_from_text_async(
            prompt=args.prompt,
            number_of_images=args.num_images,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution
        ))
    tasks.append(image_task)

    # Create the filename generation task if needed
    filename_task = None
    if not args.output_file:
        print("Generating a filename from the prompt...")
        filename_prompt = f"Generate a concise, snake_case filename (without the .png extension) for an image created with the following prompt: {args.prompt}"
        filename_task = asyncio.create_task(generate_text_async(filename_prompt))
        tasks.append(filename_task)

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)

    images = results[0]
    base_filename = args.output_file
    if filename_task:
        base_filename = results[1].strip().replace("`", "")
        # Ensure the generated filename is safe
        base_filename = "".join(c for c in base_filename if c.isalnum() or c in ('_', '-')).rstrip()
        print(f"Using generated filename: {base_filename}")


    if images:
        output_dir = Path(__file__).parent / "images" / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, img in enumerate(images):
            # Determine the effective base filename for this image
            current_base_filename = base_filename
            if len(images) > 1:
                # If multiple images are generated, append index before extension
                p = Path(base_filename)
                current_base_filename = f"{p.stem}_{i}{p.suffix}"
            else:
                current_base_filename = f"{base_filename}" # Ensure it's a string

            # Ensure the filename ends with .png
            if not current_base_filename.lower().endswith('.png'):
                current_base_filename += '.png'
            
            output_path = output_dir / current_base_filename
            counter = 0
            original_stem = Path(current_base_filename).stem
            original_suffix = Path(current_base_filename).suffix

            while output_path.exists():
                counter += 1
                new_filename_stem = f"{original_stem}_{counter}"
                output_path = output_dir / f"{new_filename_stem}{original_suffix}"
            
            img.save(output_path)
            print(f"Image saved as {output_path}")

if __name__ == "__main__":
    asyncio.run(main())