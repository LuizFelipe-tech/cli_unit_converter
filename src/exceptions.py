"""Custom exception classes for the unit converter application.

This module contains specialized exception classes used to handle specific
error scenarios such as invalid user input or out-of-range values.
"""

from __future__ import annotations


class NotAllowedValueError(Exception):
    """Exception raised when an invalid option or value is inputted.

    Raised when the user inputs an option or value that does not match
    the program's expectations.
    """
