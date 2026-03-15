"""CLI Unit Converter.

Provides an interactive command-line interface for converting units of
measurement across multiple physical categories (length, weight,
temperature, pressure, and volume).
"""

from __future__ import annotations  # noqa: I001

from typing import Final

import questionary
import typer
from loguru import logger

import core.select_menu as menu
from config.enums import UnitConverter
from config.logging_config import configure_logging
from core.convert import handle_conversion
from utils import nlp_module, validate_unit
from config import unit_definition

__version__: Final[str] = '1.2.1'
__author__: Final[str] = 'Luiz Felipe'

app = typer.Typer()

configure_logging()


@app.command()
def main(argumentos: list[str] = typer.Argument(None, help='Type your conversion request')) -> None:
    """Starts the interactive conversion workflow.

    Displays a welcome banner, presents the category selection menu,
    collects the unit pair, and delegates to the conversion handler.
    """
    try:
        unuseful_variable = unit_definition
        if argumentos:
            full_arguments = ' '.join(argumentos)
            unit_val, conversion_unit, conv_unit = nlp_module.get_value(full_arguments)
            keys = UnitConverter.get_keys_by_unit_variation(conversion_unit, conv_unit)
            units_category = validate_unit.validate_unit_categories(keys)
            handle_conversion(units_category, keys, (unit_val, True))  # pyright: ignore[reportArgumentType]

        else:
            logger.info('app_startup | version={ver}', ver=__version__)
            questionary.print('Welcome to the CLI Unit Converter!', style='bold fg:green')

            while True:
                selected_category = menu.main_menu()
                logger.debug('category_selected | category={cat}', cat=selected_category.name)

                units = menu.process_menu_selection(selected_category)
                logger.debug(
                    'units_selected | source={src} target={tgt}', src=units[0], tgt=units[1]
                    )

                handle_conversion(selected_category, units)
                logger.info('app_shutdown | graceful=True')
    except:
        logger.exception("Ocorreu um erro inesperado.")


if __name__ == '__main__':
    app()
