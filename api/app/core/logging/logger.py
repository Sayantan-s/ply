import logging
import sys
from loguru import logger

class InterceptHandler(logging.Handler):
    """
    Default handler from dev-tools to intercept standard logging messages toward your Loguru sinks.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth, 
            exception=record.exc_info
        ).bind(name=record.name).log(level, record.getMessage())

def setup_logging():
    """Initialize loguru configuration and intercept standard logs."""
    # Remove default loguru sink
    logger.remove()
    
    # Add colorful terminal sink
    # <green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{extra[name]}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # Optional: silence specific noisy loggers
    for logger_name in ("uvicorn", "uvicorn.access", "fastapi"):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = False

setup_logging()

def get_logger(name: str):
    return logger.bind(name=name)
