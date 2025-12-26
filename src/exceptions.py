"""Personalized Exceptions.

This script creates personalized exceptions used by the mains script.
"""

from __future__ import annotations


class NotAllowedValueError(Exception):
    """Raises an exception when an invalid option is inputted.

    Raised when the user inputs an option or value, which does not match
    the program’s expectation
    """
