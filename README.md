# Tools Playground

This repository is a playground for various Python scripts. The goal is to keep scripts organized and their dependencies isolated using a virtual environment.

## 1. Virtual Environment Setup and Activation

It's highly recommended to use a virtual environment to manage dependencies for these scripts.

### Create the Virtual Environment

From the root of this project, run the following command to create a virtual environment named `tools`:

```bash
python3 -m venv tools
```

### Activate the Virtual Environment

Before running any scripts or installing dependencies, activate the virtual environment.

*   **On macOS/Linux:**
    ```bash
    source tools/bin/activate
    ```

You'll know it's active when `(tools)` appears at the beginning of your terminal prompt.

## 2. Script Organization

All Python scripts should reside in the `scripts/` directory. Each script can be a standalone utility.

Example:
```
.
├── README.md
├── tools/                # Virtual environment directory
└── scripts/
    └── my_first_script.py
```

## 3. Installation of Dependencies

After activating your virtual environment, install the required Python packages using `pip` and the `requirements.txt` file.

Then, install them:

```bash
pip install -r requirements.txt
```


