"""An enumeration representing the purpose for which a number is used.

This module defines the `NumberUsedFor` enumeration, which specifies
different contexts in which a number might be utilized. It enables
a clear distinction between the number of usage types within the program.
"""

from __future__ import annotations

from enum import Enum, auto


class NumberUsedFor(Enum):
    """Enumeration defining different purposes for which a number might be used.

    Provides specific categories that can be assigned to numbers to denote their
    use case in different scenarios, such as entry input or conversion unit input.

    Attributes:
        entry_input: Indicates that the number is utilized for entry input purposes.
        conversion_unit_input: Indicates that the number is used for unit
            conversion purposes.
    """

    entry_input = auto()
    conversion_unit_input = auto()
