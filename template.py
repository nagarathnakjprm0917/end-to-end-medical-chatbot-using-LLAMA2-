import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s'
)

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    "setup.py",
    "research/trials.ipynb",
    "app.py",
    "store_index.py",
    "static/style.css",
    "templates/chat.html",
    "requirements.txt"
]

for filepath in list_of_files:
    filepath = Path(filepath)

    # Get directory and filename
    filedir = filepath.parent

    # Create directory if it doesn't exist
    if filedir != Path("."):
        filedir.mkdir(parents=True, exist_ok=True)
        logging.info(f"Creating directory: {filedir}")

    # Create empty file if it doesn't exist or is empty
    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.touch(exist_ok=True)
        logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filepath} already exists")