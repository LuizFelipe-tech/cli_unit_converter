"""Natural language parsing for unit conversion expressions.

Extracts numeric values and unit identifiers from free-text user input
using regex-based pattern matching.
"""

from __future__ import annotations

import regex
import structlog

logger = structlog.get_logger()

# Pattern: <number> <source_unit> [optional_connector] <target_unit>
NLP_REGEX = regex.compile(
    r"(?P<num>-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*(?P<unit>\p{L}+)\s+([a-zA-Z]+\s+)?(?P<conv_unit>\p{L}+)",
    regex.IGNORECASE
)


def get_value(text: str) -> tuple[float, str, str]:
    """Parse a natural language conversion expression into its components.

    Expects input in the form: ``<number> <source_unit> [connector] <target_unit>``.

    Args:
        text: A free-text string containing the conversion request
            (e.g., "100 km to miles").

    Returns:
        tuple[float, str, str]: A tuple of (numeric_value, source_unit, target_unit).
    """
    match_regex = regex.search(NLP_REGEX, text)
    if not match_regex:
        raise AttributeError("Input string did not match the expected pattern.")
    num = match_regex.group("num")
    conversion_unit = match_regex.group("unit")
    conv_unit = match_regex.group("conv_unit")
    return float(num), conversion_unit.lower(), conv_unit.lower()
