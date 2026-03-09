"""Loguru configuration for the CLI Unit Converter.

Sets up a rotating, file-based logging sink so that debug information
is captured silently without cluttering the terminal.
"""

from __future__ import annotations

from pathlib import Path

from loguru import logger

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = _PROJECT_ROOT / 'logs'
LOG_FILE = LOG_DIR / 'converter.log'

_LOG_FORMAT = '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {module}:{function}:{line} | {message}'

# Remove the default stderr sink on import so early log calls
# (e.g., unit registration in enums) stay silent.
logger.remove()


def configure_logging() -> None:
    """Adds the rotating file sink for the application.

    Call once at startup.  Logs from DEBUG upward are written to a
    rotating file; old files are compressed and kept for 7 days.
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
