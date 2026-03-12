"""CLI Unit Converter.

Provides an interactive command-line interface for converting units of
measurement across multiple physical categories (length, weight,
temperature, pressure, and volume).
"""

from __future__ import annotations

from typing import Final

from loguru import logger
import questionary
import typer

from config.logging_config import configure_logging
from core.convert import handle_conversion
import core.select_menu as menu

__version__: Final[str] = '1.2.1'
__author__: Final[str] = 'Luiz Felipe'

app = typer.Typer()

configure_logging()


@app.command()
def main(argumentos: list[str] = typer.Argument(None, help="Type your conversion request")) -> None:
    """Starts the interactive conversion workflow.

    Displays a welcome banner, presents the category selection menu,
    collects the unit pair, and delegates to the conversion handler.
    """
    if argumentos:
        full_arguments = " ". join(argumentos)
        print(full_arguments)

    logger.info('app_startup | version={ver}', ver=__version__)
    questionary.print('Welcome to the CLI Unit Converter!', style='bold fg:green')

    selected_category = menu.main_menu()
    logger.debug('category_selected | category={cat}', cat=selected_category.name)

    units = menu.process_menu_selection(selected_category)
    logger.debug('units_selected | source={src} target={tgt}', src=units[0], tgt=units[1])

    handle_conversion(selected_category, units)
    logger.info('app_shutdown | graceful=True')


if __name__ == '__main__':
    app()
