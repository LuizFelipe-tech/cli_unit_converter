"""Custom exceptions for input validation in the unit converter."""

from __future__ import annotations


class NotAllowedValueError(Exception):
    """Raised when user input falls outside the set of valid options.

    Used to signal that a syntactically valid value (e.g., an integer)
    does not correspond to any available menu or unit selection.
    """
