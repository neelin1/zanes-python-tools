This file provides guidance to coding agents when working with code in this repository.

## My Coding Guidelines

- I encourage to-the-point documentation. Use docstrings for public modules and functions.
- In-line comments in planning documents is encourage, but please avoid in-line comments explaining obvious code when you go to implement it. If the code is complex, clarification via comments is encouraged, but otherwise keep it to the docstring
- If you see the opportunity to make reusable code, do so. The `shared/` directory is the place for this.
- If there is existing documentation and you change how something works, rewrite that documentation.
- **Python**:
  - Follow PEP 8 style guidelines.
  - Use type hinting for all function definitions.
  - Keep functions small and focused on a single task.
- **Imports**:
  - Group imports by source: standard library, third-party, project modules.
  - Use absolute imports from the project root (e.g., `from shared.gemini.client import ...`).
- **Naming**:
  - Use `PascalCase` for class names.
  - Use `snake_case` for variables, functions, and module filenames.
- **Error handling**: Use `try/except` blocks for operations that can fail, like API calls or file I/O.

## Useful Reusable Code

The `shared/` directory contains code that is designed to be reusable across different scripts.

- **`shared/gemini/client.py`**: Contains the `initialize_gemini` function, which sets up the Gemini client using the API key from the `.env` file. This should be used by any script that needs to interact with the Gemini API.

- **`shared/gemini/image_generation.py`**: Provides high-level functions for generating images.
  - `generate_images_from_text()`: For text-to-image generation.
  - `generate_images_from_images()`: For image-to-image generation with one or more reference images.

## Repo Structure

- **`scripts/`**: Contains the main, executable scripts. Each major script or tool should have its own subdirectory.
  - **`scripts/nano-banana/`**: A tool for generating images with the Gemini API.
    - `main.py`: The command-line interface.
    - `playground.ipynb`: A Jupyter Notebook for interactive use.
    - `images/inputs/`: Directory for input images (ignored by git).
    - `images/outputs/`: Directory for generated images (ignored by git).
- **`shared/`**: Contains reusable, cross-cutting logic that can be used by multiple scripts.
  - **`shared/gemini/`**: Houses all Gemini-specific helper modules.
- **`.env`**: Stores secret keys, like `GEMINI_API_KEY`. This file is not committed to version control.
- **`requirements.txt`**: Lists all Python dependencies for the project.

## Commands

### Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv tools
   ```
2. Activate it:
   ```bash
   source tools/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Nano Banana CLI Usage

This script generates images using the Gemini API. All generated images are saved in the `scripts/nano-banana/images/outputs/` directory.

##### Text-to-Image
Generated images will be saved in `scripts/nano-banana/images/outputs/`.

To generate a single image with a specific aspect ratio and resolution:
```bash
# Output will be saved as scripts/nano-banana/images/outputs/city.png
python scripts/nano-banana/main.py "A futuristic cityscape" --aspect-ratio "16:9" --resolution "2K" --output-file "city.png"
```

To generate multiple images:
```bash
# Output will be saved as forest_pics_0.png, forest_pics_1.png, etc.
python scripts/nano-banana/main.py "A magical forest" --num-images 4 --output-file "forest_pics"
```

##### Image-to-Image
Place your input images in the `scripts/nano-banana/images/inputs/` directory.

To use a single reference image:
```bash
python scripts/nano-banana/main.py "Make this car look like it's flying" --input-images scripts/nano-banana/images/inputs/car.jpg
```

To use multiple reference images:
```bash
python scripts/nano-banana/main.py "Combine these two animals" --input-images scripts/nano-banana/images/inputs/cat.jpg scripts/nano-banana/images/inputs/dog.jpg
```

##### Supported Parameters

-   **Max Input Images**: Up to 14 reference images can be used for image-to-image generation.
-   **Supported Input Formats**: `PNG`, `JPEG`, `WEBP`, `HEIC`. (Note: `.heic` files are automatically converted to `.png` before processing).
-   **Supported Aspect Ratios**: `"1:1"`, `"2:3"`, `"3:2"`, `"3:4"`, `"4:3"`, `"4:5"`, `"5:4"`, `"9:16"`, `"16:9"`, `"21:9"`
-   **Supported Resolutions**: `"1K"`, `"2K"`, `"4K"`