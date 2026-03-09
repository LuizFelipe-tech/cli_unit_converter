"""CLI Unit Converter.

Converts units of measurement using a command-line interface.

This module orchestrates the user interaction, input validation, and
display of results using the 'Rich' library for a better UX. It supports
conversion logic delegated to the 'enums' module.
"""

from __future__ import annotations

from typing import Final

from loguru import logger
import questionary

from config.logging_config import configure_logging
from core.convert import handle_conversion
import core.select_menu as menu

__version__: Final[str] = '1.2.1'
__author__: Final[str] = 'Luiz Felipe'

configure_logging()


def main() -> None:
    """Starts the interactive conversion workflow.

    Displays a welcome banner, presents the category selection menu,
    collects the unit pair, and delegates to the conversion handler.
    """
    logger.info('app_startup | version={ver}', ver=__version__)
    questionary.print('Welcome to the CLI Unit Converter!', style='bold fg:green')

    selected_category = menu.main_menu()
    logger.debug('category_selected | category={cat}', cat=selected_category.name)

    units = menu.process_menu_selection(selected_category)
    logger.debug('units_selected | source={src} target={tgt}', src=units[0], tgt=units[1])

    handle_conversion(selected_category, units)
    logger.info('app_shutdown | graceful=True')


if __name__ == '__main__':
    main()
