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

    Route the execution to the specific handler functions (Length, Weight, etc.)
    based on the selected option.
    """
    valid_option: int = get_menu_option()
    # Executes conversion logic based on menu selection
    if valid_option == MENU_OPTIONS[-1]:
        console.print('[yellow]Exiting the program...[/yellow]')
        sys.exit(0)

    # Executes conversion logic based on menu selection
    match enums.Category(valid_option):
        case enums.Category.LENGTH:
            handle_length_conversion()
        case enums.Category.WEIGHT:
            handle_weight_conversion()
        case enums.Category.TEMPERATURE:
            handle_temp_conversion()
        case enums.Category.PRESSURE:
            handle_pressure_conversion()


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


def handle_temp_conversion() -> None:
    """Orchestrates the temperature conversion workflow.

    Sequence of operations:
    1. Displays available temperature units.
    2. Requests source and target unit indices.
    3. Captures the value to convert.
    4. Calls the conversion logic.
    5. Validates physical limits (e.g., Absolute Zero).
    6. Prints the formatted result.
    """
    nomes: list[str] = ['CELSIUS', 'FAHRENHEIT', 'KELVIN']
    display_units(nomes)
    entry_unit, converted_unit = request_units_number()
    input_value: float = float(
        console.input('[bold blue]Enter the number to be converted: [/bold blue]'),
    )
    converted_t = enums.UnitConverter.convert(
        input_value,
        nomes[entry_unit - 1],
        nomes[converted_unit - 1],
    )
    validate_physical_limits(3, entry_unit, input_value)
    print_conversion(converted_t, nomes[converted_unit - 1])


def handle_weight_conversion() -> None:
    """Orchestrates the weight conversion workflow.

    Sequence of operations:
    1. Displays available weight units.
    2. Requests source and target unit indices.
    3. Captures the value to convert.
    4. Calls the conversion logic.
    5. Validates physical limits (e.g., Absolute Zero).
    6. Prints the formatted result.
    """
    nomes: list[str] = ['KG', 'POUND', 'OUNCE']
    display_units(nomes)
    entry_unit, converted_unit = request_units_number()
    input_value: float = float(
        console.input('[bold blue]Enter the number to be converted: [/bold blue]'),
    )
    converted_w = enums.UnitConverter.convert(
        input_value,
        nomes[entry_unit - 1],
        nomes[converted_unit - 1],
    )
    validate_physical_limits(2, entry_unit, input_value)
    print_conversion(converted_w, nomes[converted_unit - 1])


def handle_length_conversion() -> None:
    """Orchestrates the length conversion workflow.

    Sequence of operations:
    1. Displays available length units.
    2. Requests source and target unit indices.
    3. Captures the value to convert.
    4. Calls the conversion logic.
    5. Validates physical limits (e.g., Absolute Zero).
    6. Prints the formatted result.
    """
    nomes: list[str] = ['METER', 'KM', 'MILE']
    display_units(nomes)
    entry_unit, converted_unit = request_units_number()
    input_value: float = float(
        console.input('[bold blue]Enter the number to be converted: [/bold blue]'),
    )
    converted_l = enums.UnitConverter.convert(
        input_value,
        nomes[entry_unit - 1],
        nomes[converted_unit - 1],
    )
    validate_physical_limits(1, entry_unit, input_value)
    print_conversion(converted_l, nomes[converted_unit - 1])


def handle_pressure_conversion() -> None:
    """Orchestrates the pressure conversion workflow.

    Sequence of operations:
    1. Displays available pressure units.
    2. Requests source and target unit indices.
    3. Captures the value to convert.
    4. Calls the conversion logic.
    5. Validates physical limits (e.g., Absolute Zero).
    6. Prints the formatted result.
    """
    nomes: list[str] = ['PASCAL', 'BAR', 'ATM']
    display_units(nomes)
    entry_unit, converted_unit = request_units_number()
    input_value: float = float(
        console.input('[bold blue]Enter the number to be converted: [/bold blue]'),
    )
    converted_p = enums.UnitConverter.convert(
        input_value,
        nomes[entry_unit - 1],
        nomes[converted_unit - 1],
    )
    validate_physical_limits(4, entry_unit, input_value)
    print_conversion(converted_p, nomes[converted_unit - 1])


def validate_physical_limits(category: int, source_unit: int, value: float) -> None:
    """Checks for physical and logical limits and warns the user if exceeded.

    Verifies against Absolute Zero for temperature and non-negativity for
    scalar measures (Length, Weight, Pressure). Also guards against
    computational overflow (infinity).

    Args:
        category: The main menu option (1=Length, 2=Weight, 3=Temp, 4=Pressure).
        source_unit: The ID of the source unit (used specifically in Temperature
            to determine the correct absolute zero scale).
        value: The input value to validate.
    """
    # 1. Check for Computational Limits (Infinity)
    if math.isinf(value):
        console.print(
            '[yellow][WARNING] Input is too large for standard calculation (Infinite).[/yellow]',
        )
        return

    # 2. Check for Physical Limits
    if category == MENU_OPTIONS[2]:
        # Temperature (Has specific Absolute Zero limits)
        abs_zero_limit: float = 0.0
        match source_unit:
            case 1:  # Fahrenheit
                abs_zero_limit = -459.67
            case 2:  # Celsius
                abs_zero_limit = -273.15
            case 3:  # Kelvin
                abs_zero_limit = 0.0

        if value < abs_zero_limit:
            console.print(
                f'[yellow][WARNING] Physics violation: Value is below Absolute Zero '
                f'({abs_zero_limit}).[/yellow]',
            )

    elif category in {1, 2, 4}:  # Length, Weight, Pressure (Scalar units)
        # Generally, these cannot be negative in physical measurement contexts
        if value < 0:
            console.print(
                '[yellow][WARNING] Physical limitation: '
                'This measurement usually cannot be negative.[/yellow]',
            )


def request_units_number() -> tuple[int, int]:
    """Requests the source and target unit numbers from the user.

    Loops until valid inputs are received for both the entry unit and the
    target unit.

    Returns:
      A tuple containing two integers: (valid_entry_number, valid_converted_number).
    """
    while True:
        is_valid_number, valid_entry_number = get_valid_number(is_an_entry_number=True)
        if is_valid_number:
            break
        continue
    while True:
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
        number = int(
            console.input(
                '[bold blue]Enter the origin unit number: [/bold blue]'
                if is_an_entry_number
                else '[bold blue]Enter the converted unit number: [/bold blue]',
            ),
        )
        if number not in {1, 2, 3}:
            raise exceptions.NotAllowedValueError
    except ValueError:
        console.print('[red][ERROR] PLEASE ENTER A NUMBER[/red]')
        is_valid_number = False
    except exceptions.NotAllowedValueError:
        console.print('[red][ERROR] PLEASE ENTER A VALID NUMBER[/red]')
        is_valid_number = False
    else:
        is_valid_number = True
    return is_valid_number, number


def main() -> None:
    """Main entry point of the application."""
    console.print('[green]Welcome to the CLI Unit Conversor[/green]')
    while True:
        display_main_menu()
        process_menu_selection()


if __name__ == '__main__':
    main()
