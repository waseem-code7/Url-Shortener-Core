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

def convert_to_bytes(s: str):
    try:
        return s.encode("utf-8")
    except:
        return None

def convert_to_string(s: bytes):
    try:
        return s.decode("utf-8")
    except:
        return None
