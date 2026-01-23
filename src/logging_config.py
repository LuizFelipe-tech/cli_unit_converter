"""Module for configuring structured logging for the CLI Unit Converter.

This module sets up a file-based logging system using structlog and the standard
logging library, ensuring that logs are captured silently without cluttering
the terminal output.
"""

from __future__ import annotations

import logging
from pathlib import Path

import structlog

# Path where the log will be stored
LOG_FILE = Path('../logs/converter_debug.log')


# noinspection PyTypeChecker
def configure_logging() -> None:
    """Configures silent file-based logging.

    Sets up structlog processors and a standard logging file handler to redirect
    all debug information to a local log file. This configuration ensures that
    the developer has access to the full execution history while the user
    interface remains clean.
    """
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        # Using a readable key=value format for the local log file
        structlog.dev.ConsoleRenderer(colors=False),
    ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # File Handler Configuration
    # Ensures that logs are directed to a file and not the terminal
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)

    # Reset root logger configuration to prevent printing to stdout
    root_logger = logging.getLogger()
    root_logger.handlers = [file_handler]
    root_logger.setLevel(logging.DEBUG)
