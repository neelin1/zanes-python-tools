# How to Use `nano-banana`

This script generates images using the Gemini API. All generated images are saved in the `scripts/nano-banana/images/outputs/` directory.

## Command-Line Usage

### Text-to-Image
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

### Image-to-Image
Place your input images in the `scripts/nano-banana/images/inputs/` directory.

To use a single reference image:
```bash
python scripts/nano-banana/main.py "Make this car look like it's flying" --input-images scripts/nano-banana/images/inputs/car.jpg
```

To use multiple reference images:
```bash
python scripts/nano-banana/main.py "Combine these two animals" --input-images scripts/nano-banana/images/inputs/cat.jpg scripts/nano-banana/images/inputs/dog.jpg
```