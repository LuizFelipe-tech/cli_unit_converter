"""Custom exceptions for input validation."""

from __future__ import annotations


class NotAllowedValueError(Exception):
    """Raised when user input is not among the valid options."""
