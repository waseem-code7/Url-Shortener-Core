import json
import logging
logging.basicConfig(level=logging.INFO)

def get_logger(file_name: str) -> logging.Logger:
    return logging.getLogger(file_name)

def stringify(d: dict) -> str:
    try:
        return json.dumps(d)
    except Exception as e:
        return ""
