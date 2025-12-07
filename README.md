# Tools Playground

This repository is a playground for various Python scripts. The goal is to keep scripts organized and in one place thats easily accessible by AI CLI Agents

## Set-up

### 1. Virtual Environment Setup and Activation

It's highly recommended to use a virtual environment to manage dependencies for these scripts.

#### Create the Virtual Environment

From the root of this project, run the following command to create a virtual environment named `tools`:

```bash
python3 -m venv tools
```

#### Activate the Virtual Environment

Before running any scripts or installing dependencies, activate the virtual environment.

- **On macOS/Linux:**
  ```bash
  source tools/bin/activate
  ```

You'll know it's active when `(tools)` appears at the beginning of your terminal prompt.

### 2. API Key Setup

Create a `.env` file in the root of the project to store your Gemini API key.

```bash
touch .env
```

Now, open the `.env` file and add the following line, replacing `YOUR_GEMINI_API_KEY` with your actual key:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

### 3. Installation of Dependencies

After activating your virtual environment, install the required Python packages using `pip` and the `requirements.txt` file.


```bash
pip install -r requirements.txt
```

## Script Organization

All Python scripts should reside in the `scripts/` directory. Each script can be a standalone utility.

### Nano Banana

The `nano-banana` script is a tool for generating images using the Google Gemini API. It supports text-to-image, image-to-image, and multi-image prompts, with options for aspect ratio and resolution.

It can be used in three ways:

- **AI CLI USAGE**: Recommended way. Enter something like, "please upscale this using nanobananba /Users/neelin2/coding/tools/scripts/nano-banana/images/inputs/ranier.webp", and Claude Code will do a pretty good job at running the script for you. Claude code, Gemini CLI, and Codex CLI are supported. Specifying aspect ratio and resolution is often useful.
- **CLI Usage**: Run the script from your terminal to generate images. For example:
  ```bash
  python scripts/nano-banana/main.py "A beautiful oil painting of a sunset over the ocean" --aspect-ratio "16:9"
  ```
- **Jupyter Notebook**: For a more interactive experience, open and run the cells in `scripts/nano-banana/playground.ipynb`.

For detailed instructions on all the available commands and parameters, please see the [**USAGE.md**](scripts/nano-banana/USAGE.md) file inside the `nano-banana` directory.

```
.
├── README.md
├── tools/                # Virtual environment directory
└── scripts/
    └── nano-banana/
        ├── main.py
        ├── playground.ipynb
        └── USAGE.md
```
