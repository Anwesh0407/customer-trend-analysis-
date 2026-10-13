"""
AVA Structured Logging Setup with Secret Masking
"""

import logging
import sys
import re
from ava.config import settings

SECRET_PATTERNS = [
    re.compile(r'(password=)[^\s&]+', re.IGNORECASE),
    re.compile(r'(key=)[^\s&]+', re.IGNORECASE),
    re.compile(r'(secret=)[^\s&]+', re.IGNORECASE),
    re.compile(r'(bearer\s+)[a-zA-Z0-9_\-\.]+', re.IGNORECASE)
]

class MaskingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        for pattern in SECRET_PATTERNS:
            msg = pattern.sub(r'\1[MASKED]', msg)
        return msg

def get_logger(name: str = "ava") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            MaskingFormatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    return logger

def configure_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            MaskingFormatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

logger = get_logger("ava")
