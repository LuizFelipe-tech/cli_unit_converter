"""Natural language parsing for unit conversion expressions.

Extracts numeric values and unit identifiers from free-text user input
using regex-based pattern matching.
"""

from __future__ import annotations

import regex

# Pattern: <number> <source_unit> [optional_connector] <target_unit>
NLP_REGEX = regex.compile(r'(?P<num>\d+)\s*(?P<unit>\p{L}+)\s([a-zA-Z]+\s)?(?P<conv_unit>\p{L}+)')


def get_value(text: str) -> tuple[int, str, str]:
    """Parse a natural language conversion expression into its components.

    Expects input in the form: ``<number> <source_unit> [connector] <target_unit>``.

    Args:
        text: A free-text string containing the conversion request
            (e.g., "100 km to miles").

    Returns:
        tuple[int, str, str]: A tuple of (numeric_value, source_unit, target_unit).
    """
    match_regex = regex.search(NLP_REGEX, text)
    num = match_regex.group('num')
    conversion_unit = match_regex.group('unit')
    conv_unit = match_regex.group('conv_unit')
    return int(num), conversion_unit, conv_unit
