from __future__ import annotations

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ExtractionConfig:
    model_name: str = 'en_core_web_lg'
    fuzzy_threshold: int = 80
    target_skills: List[str] = field(defaul_factory)
