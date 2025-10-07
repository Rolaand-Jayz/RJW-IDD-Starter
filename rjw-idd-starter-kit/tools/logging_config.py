"""Centralized logging configuration for RJW-IDD."""

import logging
import logging.config
from pathlib import Path
from typing import Any, Optional


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "logs/rjw_idd.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
    "loggers": {
        "rjw_idd": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    verbose: bool = False,
) -> None:
    """Configure logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        verbose: Enable verbose output
    """
    # Create a deep copy of the config to avoid modifying the original
    import copy
    config: dict[str, Any] = copy.deepcopy(LOGGING_CONFIG)

    # Set log level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    config["root"]["level"] = numeric_level

    # Update file handler if log_file specified
    if log_file:
        config["handlers"]["file"]["filename"] = str(log_file)

    # Enable verbose mode
    if verbose:
        config["handlers"]["console"]["level"] = "DEBUG"
        config["handlers"]["console"]["formatter"] = "detailed"

    # Apply configuration
    logging.config.dictConfig(config)

    # Log setup completion
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level {level}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(f"rjw_idd.{name}")
