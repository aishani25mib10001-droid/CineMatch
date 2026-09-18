"""
logger_config.py
-----------------
Provides a single shared logger for the whole application.
Every module that wants to log something calls get_logger(__name__)
instead of configuring logging itself. This satisfies the
Logging / Monitoring non-functional requirement and keeps log
formatting consistent across the codebase.
"""

import logging
from src.config import LOG_PATH


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:  # avoid duplicate handlers on repeated calls
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(LOG_PATH)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.WARNING)  # keep CLI output clean

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
