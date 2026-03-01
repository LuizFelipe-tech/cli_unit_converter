"""Classes and functions related to the NLP module."""

from __future__ import annotations

from dataclasses import dataclass

import structlog

logger = structlog.get_logger()


@dataclass(frozen=True)
class ExtractionConfig:
    """Stores NLP info."""
    model_name: str = 'en_core_web_lg'
    fuzzy_threshold: int = 80
