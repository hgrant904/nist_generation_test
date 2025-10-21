"""Logging configuration for the application."""

import logging
import sys

from app.core.settings import settings


def setup_logging() -> None:
    """Configure application logging."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.DEBUG if settings.DATABASE_ECHO else logging.WARNING
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)
