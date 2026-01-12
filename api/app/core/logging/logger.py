import logging

def get_logger(name: str):
    return logging.getLogger(f"app.{name}")
