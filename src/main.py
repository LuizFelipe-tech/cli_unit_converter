"""CLI Unit Converter.

Converts units of measurement using a command-line interface.

This module orchestrates the user interaction, input validation, and
display of results using the 'Rich' library for a better UX. It supports
conversion logic delegated to the 'enums' module.
"""

from __future__ import annotations

from typing import Final

from loguru import logger
from rich.console import Console
from rich.traceback import install

from config.logging_config import configure_logging
from core.convert import handle_conversion
import core.select_menu as menu

__version__: Final[str] = '1.2.1'
__author__: Final[str] = 'Luiz Felipe'

configure_logging()

console = Console()


def main() -> None:
    """Entry point that starts the interactive conversion loop.

    Initializes logging, displays a welcome message, and continuously
    presents the main menu until the user exits.
    """
    logger.info('app_startup | version={ver}', ver=__version__)
    console.print('[green]Welcome to the CLI Unit Converter[/green]')
    selected_category = menu.main_menu()
    units = menu.process_menu_selection(selected_category)
    handle_conversion(selected_category, units)


if __name__ == '__main__':
    install(show_locals=True)
    main()
