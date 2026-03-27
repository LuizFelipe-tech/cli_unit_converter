"""Validation utilities for unit categories.

Ensures that unit pairs belong to the same physical category before
proceeding with conversions.
"""

from __future__ import annotations

from config.enums import UnitConverter


def validate_unit_categories(keys: list[str]):
    """Validates that all provided unit keys belong to the same category.

    Args:
        keys: A list of registered unit keys to validate.

    Returns:
        The ``Category`` shared by all units, or ``None`` if they belong
        to different categories.
    """
    if not keys or any(k is None for k in keys):
        return None

    categories = [UnitConverter.get_unit_info(key).category for key in keys]
    first_category = categories[0]
    if any(x != first_category for x in categories):
        return None
    return first_category
