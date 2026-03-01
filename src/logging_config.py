"""Module for configuring structured logging for the CLI Unit Converter.

This module sets up a file-based logging system using Loguru, ensuring that
debug information is captured silently to a rotating log file without
cluttering the terminal output.
"""

from __future__ import annotations

from pathlib import Path

from loguru import logger

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = _PROJECT_ROOT / 'logs'
LOG_FILE = LOG_DIR / 'converter.log'

_LOG_FORMAT = '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {module}:{function}:{line} | {message}'

# Remove the default stderr sink immediately on import so that any module
# imported after this one (e.g. enums, which registers units at import time)
# does not leak debug output to the terminal.
logger.remove()


def configure_logging() -> None:
    """Configures silent file-based logging with Loguru.

    Adds a rotating file sink that captures everything from DEBUG upwards.
    Old log files are compressed and kept for 7 days. The default stderr sink
    is already removed at module-import time (see above) so that early log
    calls during other module imports stay silent.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger.add(
        LOG_FILE,
        format=_LOG_FORMAT,
        level='DEBUG',
        rotation='5 MB',
        retention='7 days',
        compression='zip',
        backtrace=True,
        diagnose=True,
        encoding='utf-8',
    )
