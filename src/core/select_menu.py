"""Interactive menus for category and unit selection.

Uses ``questionary`` prompts to guide the user through choosing a
physical category and a source/target unit pair.
"""

from __future__ import annotations

from loguru import logger
import questionary

from config import enums


def main_menu() -> enums.Category:
    """Displays the category selection menu.

    Returns:
        The selected ``Category`` enum member.
    """
    category_display: dict[enums.Category, str] = {cat: cat.display_name for cat in enums.Category}

    option = questionary.select(
        'Which category do you want to convert?',
        choices=list(category_display.values()),
    ).ask()

    selected = next(k for k, v in category_display.items() if v == option)
    logger.debug('main_menu_choice | category={cat}', cat=selected.name)
    return selected


def process_menu_selection(option_selected: enums.Category) -> tuple[str, str]:
    """Retrieves the available units and prompts for a pair.

    Args:
        option_selected: The chosen ``Category`` enum member.

    Returns:
        A ``(source_key, target_key)`` tuple of unit registry keys.
    """
    units_keys = enums.UnitConverter.get_keys_by_category(option_selected)
    return get_units(units_keys)


def get_units(keys: list[str]) -> tuple[str, str]:
    """Prompts the user to pick source and target units.

    Re-prompts when the user selects the same unit for both source
    and target.

    Args:
        keys: List of unit registry keys available for selection.

    Returns:
        A ``(source_key, target_key)`` tuple.
    """
    while True:
        source = questionary.select('Select the source unit:', choices=keys).ask()
        target = questionary.select('Select the target unit:', choices=keys).ask()

        if source == target:
            logger.debug('duplicate_unit_selection | unit={u}', u=source)
            questionary.print(
                'Source and target units must be different. Try again.',
                style='bold fg:yellow',
            )
            continue

        logger.debug('unit_pair_confirmed | source={s} target={t}', s=source, t=target)
        return source, target
