"""Classes and functions related to the NLP module."""

from __future__ import annotations

from dataclasses import dataclass

import regex
import structlog

logger = structlog.get_logger()

NLP_REGEX = regex.compile(r'(?P<num>\d+)\s*(?P<unit>\p{L}+)\s([a-zA-Z]+\s)?(?P<conv_unit>\p{L}+)')


def get_value(text: str) -> tuple[int, str, str]:
    """Handle the user input text.

    Args:
        text: a string contaiming the user input
    Returns:
        tuple: a tuple containing a number, the unit to converted, unit to convert
    """
    match_regex = regex.search(NLP_REGEX, text)
    num = match_regex.group('num')
    conversion_unit = match_regex.group('unit')
    conv_unit = match_regex.group('conv_unit')
    return int(num), conversion_unit, conv_unit
