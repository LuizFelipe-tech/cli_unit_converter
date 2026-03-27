#!/usr/bin/env python3
"""CLI Unit Converter.

Provides an interactive command-line interface for converting units of
measurement across multiple physical categories (length, weight,
temperature, pressure, and volume).
"""

from __future__ import annotations  # noqa: I001

from typing import Final

import typer
from loguru import logger

import core.select_menu as menu
from config.enums import UnitConverter
from config.logging_config import configure_logging
from core.convert import handle_conversion
from utils import nlp_module, validate_unit
from config import unit_definition  # noqa: F401 (Registers units)

__version__: Final[str] = '2.1.0'
__author__: Final[str] = 'Luiz Felipe'

app = typer.Typer()

configure_logging()


@app.command()
def main(args: list[str] = typer.Argument(None, help='Type your conversion request')) -> None:
    """Starts the interactive conversion workflow.

    Displays a welcome banner, presents the category selection menu,
    collects the unit pair, and delegates to the conversion handler.
    """
    try:
        logger.debug(f'Registry size at start: {len(UnitConverter._registry)}')
        if args:
            full_arguments = ' '.join(args)
            unit_val, conversion_unit, conv_unit = nlp_module.get_value(full_arguments)
            keys = UnitConverter.get_keys_by_unit_variation(conversion_unit, conv_unit)
            if None in keys:
                logger.warning('unit_not_found | keys={keys}', keys=keys)
                typer.secho(
                    'One or more units were not recognized. Please check your spelling.',
                    fg=typer.colors.RED,
                    bold=True,
                )
                return

            units_category = validate_unit.validate_unit_categories(keys)
            handle_conversion(units_category, keys, (unit_val, True))  # pyright: ignore[reportArgumentType]

        else:
            logger.info('app_startup | version={ver}', ver=__version__)
            typer.secho('Welcome to the CLI Unit Converter!', fg=typer.colors.GREEN, bold=True)

            while True:
                selected_category = menu.main_menu()
                logger.debug('category_selected | category={cat}', cat=selected_category.name)

                units = menu.process_menu_selection(selected_category)
                logger.debug(
                    'units_selected | source={src} target={tgt}', src=units[0], tgt=units[1]
                )

                handle_conversion(selected_category, units)
                logger.info('app_shutdown | graceful=True')
    except Exception:
        logger.exception('An unexpected error occurred.')


if __name__ == '__main__':
    app()
