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

__version__ = '1.1.0'


def get_menu_options() -> list[int]:
    """Returns the list of valid menu options based on registered categories.

    Returns:
        list[int]: A list of integers representing valid menu selections.
    """
    return [i.value for i in enums.Category] + [len(enums.Category) + 1]


def display_main_menu() -> None:
    """Displays the main menu options to the standard output."""
    menu_lines = []
    for category in enums.Category:
        units = enums.UnitConverter.get_keys_by_category(category)
        names = [enums.UnitConverter.get_unit_info(k).name.split()[-1] for k in units]
        units_str = ' :left_right_arrow: '.join(names)
        menu_lines.append(f'{category.value}. {category.display_name} ({units_str})')

    exit_option = len(enums.Category) + 1
    menu_lines.append(f'{exit_option}. Exit')

    menu_content = '\n'.join(menu_lines)
    print()
    console.print(Panel(menu_content, title='[bold blue]Main Menu[/bold blue]', expand=False))


def get_menu_option() -> int:
    """Prompts the user to select a category from the main menu.

    Loops continuously until a valid integer is received.
    Handles noninteger inputs and values outside the allowed range internally.

    Returns:
        int: The selected menu option.
    """
    valid_options = get_menu_options()
    while True:
        try:
            selected_option: int = int(
                console.input('[bold blue]Enter the number for the selected option: [/bold blue]'),
            )
            if selected_option not in valid_options:
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

    Routes the execution to the specific handler functions based on the selected option.
    """
    valid_option: int = get_menu_option()
    exit_option = len(enums.Category) + 1
    # Execute conversion logic based on menu selection.
    if valid_option == exit_option:
        console.print('[yellow]Exiting the program...[/yellow]')
        sys.exit(0)

    selected_category = enums.Category(valid_option)
    units_keys = enums.UnitConverter.get_keys_by_category(selected_category)
    handle_conversion(selected_category, units_keys)


def display_units(category: enums.Category, keys: list[str]) -> None:
    """Displays the available units for the selected category.

    Prints a header identifying the category and lists the units with their
    corresponding selection numbers based on the provided registry keys.

    Args:
        category (enums.Category): The selected physical category.
        keys (list[str]): A list of strings representing the keys in the UnitConverter
            registry (e.g., ['METER', 'KM', 'MILE']).
    """
    console.print()
    console.print(f'[green]--- {category.display_name} Converter selected ---[/green]')
    console.print('Available units below')
    for i, key in enumerate(keys, start=1):
        console.print(f'{i}. {enums.UnitConverter.get_unit_info(key).name.split()[-1]}')


def print_conversion(converted_value: float, unit_key: str) -> None:
    """Formats and prints the final conversion result using Rich.

    Retrieves the plural name of the target unit from the registry to ensure
    grammatically correct output.

    Args:
        converted_value (float): The numeric result of the conversion.
        unit_key (str): The registry key of the target unit (to fetch its display name).
    """
    unit_plural = enums.UnitConverter.get_unit_info(unit_key).plural
    unit_singular = enums.UnitConverter.get_unit_info(unit_key).name
    console.print(
        f'[bold green]Result:[/bold green] [yellow]{converted_value:.2f}[/yellow]'
        f' {unit_singular if converted_value in {0, 1} else unit_plural}',
    )


def handle_conversion(category: enums.Category, units_keys: list[str]) -> None:
    """Orchestrates a generic conversion workflow for any category.

    This function abstracts the repetition found in specific handlers.
    It guides the user through selecting units from the provided list,
    inputting values, performing the conversion, and viewing the result,
    while enforcing category-specific physical limits.

    Args:
        category (enums.Category): The category enum member (e.g., Category.LENGTH) is used
            to determine specific validation rules (like absolute zero).
        units_keys (list[str]): A list of string keys representing the available units
            in the registry for this category (e.g., ['METER', 'KM']).
    """
    # 1. Dynamically display units
    display_units(category, units_keys)

    # 2. Get inputs
    max_units = len(units_keys)
    entry_index, target_index = request_units_number(max_units)

    input_value: float = float(
        console.input('[bold blue]Enter the number to be converted: [/bold blue]'),
    )

    # 3. Map the chosen index to the real key ('CELSIUS', etc.)
    source_key = units_keys[entry_index - 1]
    target_key = units_keys[target_index - 1]

    # 4. Convert
    result = enums.UnitConverter.convert(input_value, source_key, target_key)

    # 5. Validation
    validate_physical_limits(category, source_key, input_value)

    # 6. Print
    print_conversion(result, target_key)


def validate_physical_limits(category: enums.Category, unit_key: str, value: float) -> None:
    """Checks for physical/logical limits and warns if exceeded.

    Verifies against Absolute Zero for temperature and non-negativity
    for scalar measures (Length, Weight, Pressure). Guards against
    computational overflow (infinity).

    Args:
        category (enums.Category): The category enum member (e.g., Category.TEMPERATURE).
        unit_key (str): The registry key of the source unit (e.g., 'CELSIUS',
            'FAHRENHEIT'). Used to look up specific physical limits.
        value (float): The input value to validate.
    """
    # 1. Check for Computational Limits (Infinity)
    if math.isinf(value):
        console.print(
            '[yellow][WARNING] Input is too large for standard calculation (Infinite).[/yellow]',
        )
        return

    # 2. Check for Physical Limits
    min_base = category.min_value_base
    if min_base is not None:
        unit_info = enums.UnitConverter.get_unit_info(unit_key)
        value_in_base = unit_info.to_base(value)

        if value_in_base < min_base:
            min_in_unit = unit_info.from_base(min_base)
            # Round for display
            min_in_unit = round(min_in_unit, 2)
            console.print(
                f'[yellow][WARNING] Physical limitation: Value is below '
                f'minimum possible ({min_in_unit} {unit_info.plural}).[/yellow]',
            )


def request_units_number(max_units: int) -> tuple[int, int]:
    """Requests the source and target unit numbers from the user.

    Loops until valid inputs are received for both the entry unit and the
    target unit.

    Args:
        max_units (int): The maximum allowed unit number.

    Returns:
        tuple[int, int]: A tuple containing the valid entry unit number and
            converted unit number.
    """
    while True:
        # Get and validate the origin unit.
        is_valid_number, valid_entry_number = get_valid_number(
            is_an_entry_number=True,
            max_value=max_units,
        )
        if is_valid_number:
            break
    while True:
        # Get and validate the target unit.
        is_valid_number, valid_converted_number = get_valid_number(
            is_an_entry_number=False,
            max_value=max_units,
        )
        if is_valid_number:
            break
    return valid_entry_number, valid_converted_number


def get_valid_number(*, is_an_entry_number: bool, max_value: int) -> tuple[bool, int]:
    """Gets and validates a single unit selection from user input.

    Ensures the user enters a number corresponding to an available unit.

    Args:
        is_an_entry_number (bool): If True, prompts for the 'origin' unit.
            If False, prompts for the 'target' unit.
        max_value (int): The maximum allowed unit number.

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

        # Check if the entered number is within the allowed unit range.
        if not (1 <= number <= max_value):
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
