import logging
logging.basicConfig(level=logging.INFO)

def get_logger(file_name: str) -> logging.Logger:
    return logging.getLogger(file_name)

