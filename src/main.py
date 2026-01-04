"""CLI Unit Converter.

Converts units of measurement using a command-line interface.

This module orchestrates the user interaction, input validation, and
display of results using the 'Rich' library for a better UX. It supports
conversion logic delegated to the 'enums' module.
"""

from __future__ import annotations

import math
import sys

from rich.console import Console
from rich.panel import Panel

import enums
import exceptions

console = Console()

__version__ = '1.0.0'

MENU_OPTIONS = [1, 2, 3, 4, 5]


def display_main_menu() -> None:
    """Displays the main menu options to the standard output."""
    menu_content = (
        '1. Length (Meters :left_right_arrow: Kilometers :left_right_arrow: Miles)\n'
        '2. Weight (Kilograms :left_right_arrow: Pound :left_right_arrow: Ounces)\n'
        '3. Temperature (Celsius :left_right_arrow: Fahrenheit :left_right_arrow: Kelvin)\n'
        '4. Pressure (Pascal :left_right_arrow: Atmosphere :left_right_arrow: Bar)\n'
        '5. Exit'
    )
    console.print(Panel(menu_content, title='[bold blue]Main Menu[/bold blue]', expand=False))


def get_menu_option() -> int:
    """Prompts the user to select a category from the main menu.

    Loops continuously until a valid integer between 1 and 5 is received.
    Handles noninteger inputs and values outside the allowed range internally.

    Returns:
        int: The selected menu option (1: Length, 2: Weight, 3: Temperature,
        4: Pressure, 5: Exit).
    """
    while True:
        try:
            selected_option: int = int(
                console.input('[bold blue]Enter the number for the selected option: [/bold blue]'),
            )
            if selected_option not in MENU_OPTIONS:
                raise exceptions.NotAllowedValueError
        except exceptions.NotAllowedValueError:  # noqa: PERF203
            console.print('[bold red][ERROR] PLEASE ENTER A VALID NUMBER [/bold red]')
        except ValueError:
            console.print('[bold red][ERROR] PLEASE ENTER A NUMBER[/bold red]')
        else:
            break
    return selected_option


def process_menu_selection() -> None:
    """Processes the user's menu selection and triggers conversion flows.

    Routes the execution to the specific handler functions (Length, Weight, etc.)
    based on the selected option.
    """
    valid_option: int = get_menu_option()
    # Execute conversion logic based on menu selection.
    if valid_option == MENU_OPTIONS[-1]:
        console.print('[yellow]Exiting the program...[/yellow]')
        sys.exit(0)
    selected_category = enums.Category(valid_option)
    # Match the selected category to its respective unit keys.
    match selected_category:
        case enums.Category.LENGTH:
            handle_conversion(selected_category, ['METER', 'KM', 'MILE'])
        case enums.Category.WEIGHT:
            handle_conversion(selected_category, ['KG', 'POUND', 'OUNCE'])
        case enums.Category.TEMPERATURE:
            handle_conversion(selected_category, ['CELSIUS', 'FAHRENHEIT', 'KELVIN'])
        case enums.Category.PRESSURE:
            handle_conversion(selected_category, ['PASCAL', 'BAR', 'ATM'])


def display_units(keys: list[str]) -> None:
    """Displays the available units for the selected category.

    Prints a header identifying the category and lists the units with their
    corresponding selection numbers based on the provided registry keys.

    Args:
        keys: A list of strings representing the keys in the UnitConverter
            registry (e.g., ['METER', 'KM', 'MILE']).
    """
    console.print()
    console.print(
        f'[green]--- {enums.UnitConverter.registry[keys[0]].category_name} '
        'Converter selected ---[/green]',
    )
    console.print('Available units below')
    for i, key in enumerate(keys, start=1):
        console.print(f'{i}. {enums.UnitConverter.registry[key].name.split()[-1]}')


def print_conversion(converted_value: float, unit_key: str) -> None:
    """Formats and prints the final conversion result using Rich.

    Retrieves the plural name of the target unit from the registry to ensure
    grammatically correct output.

    Args:
        converted_value: The numeric result of the conversion.
        unit_key: The registry key of the target unit (to fetch its display name).
    """
    unit_plural = enums.UnitConverter.get_unit_info(unit_key).plural
    console.print(
        f'[bold green]Result:[/bold green] [yellow]{converted_value}[/yellow] {unit_plural}',
    )


def handle_conversion(category: enums.Category, units_keys: list[str]) -> None:
    """Orchestrates a generic conversion workflow for any category.

    This function abstracts the repetition found in specific handlers.
    It guides the user through selecting units from the provided list,
    inputting values, performing the conversion, and viewing the result,
    while enforcing category-specific physical limits.

    Args:
        category: The category enum member (e.g., Category.LENGTH) is used
            to determine specific validation rules (like absolute zero).
        units_keys: A list of string keys representing the available units
            in the registry for this category (e.g., ['METER', 'KM']).
    """
    # 1. Dynamically display units
    display_units(units_keys)

    # 2. Get inputs
    entry_index, target_index = request_units_number()

    # Validates if the indices are within the real list size
    if not (1 <= entry_index <= len(units_keys)) or not (1 <= target_index <= len(units_keys)):
        console.print('[bold red]Invalid unit option![/bold red]')
        return

    input_value: float = float(
        console.input('[bold blue]Enter the number to be converted: [/bold blue]'),
    )

    # 3. Map the chosen index (1, 2, 3) to the real key ('CELSIUS', etc.)
    source_key = units_keys[entry_index - 1]
    target_key = units_keys[target_index - 1]

    # 4. Convert
    result = enums.UnitConverter.convert(input_value, source_key, target_key)

    # 5. Validation (We pass the KEY, not the number, to be safer)
    validate_physical_limits(category, source_key, input_value)

    # 6. Print
    print_conversion(result, target_key)


def validate_physical_limits(
    category: enums.Category,
    unit_key: str,
    value: float,
) -> None:
    """Checks for physical/logical limits and warns if exceeded.

    Verifies against Absolute Zero for temperature and non-negativity
    for scalar measures (Length, Weight, Pressure). Guards against
    computational overflow (infinity).

    Args:
        category: The category enum member (e.g., Category.TEMPERATURE).
        unit_key: The registry key of the source unit (e.g., 'CELSIUS',
            'FAHRENHEIT'). Used to look up specific physical limits.
        value: The input value to validate.
    """
    # 1. Check for Computational Limits (Infinity)
    if math.isinf(value):
        console.print(
            '[yellow][WARNING] Input is too large for standard calculation (Infinite).[/yellow]',
        )
        return

    # 2. Check for Physical Limits
    if category == enums.Category.TEMPERATURE:
        # Dictionary mapping unit keys to their Absolute Zero limit
        abs_zero_limits: dict[str, float] = {
            'FAHRENHEIT': -459.67,
            'CELSIUS': -273.15,
            'KELVIN': 0.0,
        }

        # Uses .get() to prevent crashes if a key is missing (defensive coding)
        limit = abs_zero_limits.get(unit_key)

        if limit is not None and value < limit:
            console.print(
                f'[yellow][WARNING] Physics violation: Value is below Absolute '
                f'Zero ({limit}).[/yellow]',
            )

    # For scalar units (Length, Weight, Pressure), values usually cannot be negative.
    # We check if the category is NOT temperature.
    elif value < 0:
        console.print(
            '[yellow][WARNING] Physical limitation: '
            'This measurement usually cannot be negative.[/yellow]',
        )


def request_units_number() -> tuple[int, int]:
    """Requests the source and target unit numbers from the user.

    Loops until valid inputs are received for both the entry unit and the
    target unit.

    Returns:
        tuple[int, int]: A tuple containing the valid entry unit number and
            converted unit number.
    """
    while True:
        # Get and validate the origin unit.
        is_valid_number, valid_entry_number = get_valid_number(is_an_entry_number=True)
        if is_valid_number:
            break
        continue
    while True:
        # Get and validate the target unit.
        is_valid_number, valid_converted_number = get_valid_number(is_an_entry_number=False)
        if is_valid_number:
            break
        continue
    return valid_entry_number, valid_converted_number


def get_valid_number(*, is_an_entry_number: bool) -> tuple[bool, int]:
    """Gets and validates a single unit selection from user input.

    Ensures the user enters a number corresponding to an available unit
    (currently hardcoded to indices 1, 2, or 3).

    Args:
        is_an_entry_number: If True, prompts for the 'origin' unit.
            If False, prompts for the 'target' unit.

    Returns:
        tuple[bool, int]: A tuple containing:
            - bool: True if the input was valid, False otherwise.
            - int: The parsed unit number (or 0 if invalid).
    """
    number: int = 0
    try:
        # Prompt the user for input based on whether it's an origin or target unit.
        prompt = (
            '[bold blue]Enter the origin unit number: [/bold blue]'
            if is_an_entry_number
            else '[bold blue]Enter the converted unit number: [/bold blue]'
        )
        number = int(console.input(prompt))

        # Check if the entered number is within the allowed unit range (1-3).
        if number not in {1, 2, 3}:
            raise exceptions.NotAllowedValueError
    except ValueError:
        # Handle cases where the input is not a valid integer.
        console.print('[red][ERROR] PLEASE ENTER A NUMBER[/red]')
        is_valid_number = False
    except exceptions.NotAllowedValueError:
        # Handle cases where the number is an integer but not a valid option.
        console.print('[red][ERROR] PLEASE ENTER A VALID NUMBER[/red]')
        is_valid_number = False
    else:
        # Input is valid and within range.
        is_valid_number = True
    return is_valid_number, number


def main() -> None:
    """Main entry point of the application."""
    console.print('[green]Welcome to the CLI Unit Converter[/green]')
    while True:
        display_main_menu()
        process_menu_selection()


if __name__ == '__main__':
    main()
