import logging
import json
import os

logger = logging.getLogger(__name__)

def save_json(data: dict, filename: str, output_dir: str):
    raw_dir = os.path.join(output_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)
    filepath = os.path.join(raw_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logger.info(f"Saved JSON output to {filepath}")