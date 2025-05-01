import logging
logging.basicConfig(level=logging.INFO)

def get_logger(file_name: str) -> logging:
    return logging.getLogger(file_name)

