from __future__ import annotations

import structlog
from dataclasses import dataclass, field
from typing import List

logger = structlog.get_logger()


@dataclass(frozen=True)
class ExtractionConfig:
    model_name: str = 'en_core_web_lg'
    fuzzy_threshold: int = 80
    target_skills: List[str] = field(default_factory=list)
