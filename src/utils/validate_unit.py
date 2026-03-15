from __future__ import annotations

from config.enums import UnitConverter


def validate_unit_categories(keys):
    """Validates if the provided unit keys belong to distinct categories.

    Checks the category for each unit key in the provided list. If any two keys
    belong to the same category, the validation fails.

    Args:
        keys: An iterable of registered unit keys to validate.

    Returns:
        A list of categories corresponding to each unit key if all categories are
        unique. Returns None if there are duplicate categories.
    """
    categories = [UnitConverter.get_unit_info(key).category for key in keys]
    first_category = categories[0]
    if any(x != first_category for x in categories):
        return None
    return first_category
