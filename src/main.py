"""CLI Unit Converter.

Converts units of measurement using a command-line interface. Supports conversion
between different systems for length, weight and temperature.
"""

from __future__ import annotations

import math
import sys

import enums
import exceptions

__version__ = '1.0.0'

BIDIRECTIONAL_ARROW = '\u2194'

RED_TEXT = '\x1b[31m'

GREEN_TEXT = '\x1b[32m'

YELLOW_TEXT = '\033[33m'

RESET = '\x1b[0m'


def display_main_menu() -> None:
    """Displays the main menu options to the standard output."""
    print()
    print(f'1. Length (Meters {BIDIRECTIONAL_ARROW} Kilometers {BIDIRECTIONAL_ARROW} Miles)')
    print(f'2. Weight (Kilograms {BIDIRECTIONAL_ARROW} Pound {BIDIRECTIONAL_ARROW} Ounces)')
    print(f'3. Temperature (Celsius {BIDIRECTIONAL_ARROW} Fahrenheit {BIDIRECTIONAL_ARROW} Kelvin)')
    print(f'4. Pressure (Pascal {BIDIRECTIONAL_ARROW} Atmosphere {BIDIRECTIONAL_ARROW} Bar)')
    print('5. Exit')


def get_menu_option() -> int:
    """Gets a valid menu option.

    Loops until valid inputs are received for both the entry unit and the
    target unit.

    Returns:
        A valid menu option (int)
    """
    while True:
        try:
            selected_option: int = int(input('Enter the number for the selected option: '))
            if selected_option not in {1, 2, 3, 4, 5}:
                raise exceptions.NotAllowedValueError
        except exceptions.NotAllowedValueError:  # noqa: PERF203
            print(f'{RED_TEXT}[ERROR] PLEASE ENTER A VALID NUMBER{RESET}')
        except ValueError:
            print(f'{RED_TEXT}[ERROR] PLEASE ENTER A NUMBER{RESET}')
        else:
            break
    return selected_option


def process_menu_selection() -> None:
    """Processes the menu selection.

    Runs the corresponding conversion logic. Handles
    invalid inputs internally by catching exceptions and printing error messages.
    """
    valid_option: int = get_menu_option()
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
        case _:
            print(f'{YELLOW_TEXT}Exiting the program...{RESET}')
            sys.exit(0)


def display_units(keys: list[str]) -> None:
    print()
    print(
        f'{GREEN_TEXT}'
        f'--- {enums.UnitConverter.registry[keys[0]].category_name} Converter selected ---'
        f'{RESET}',
    )
    print('Available units below')
    for i, key in enumerate(keys, start=1):
        print(f'{i}. {enums.UnitConverter.registry[key].name.split()[-1]}')


def print_conversion(converted_unit: float) -> None:
    unit_plural = enums.UnitConverter.get_unit_info('METER').plural
    print(f'{converted_unit} {unit_plural}')


def handle_temp_conversion() -> None:
    """Orchestrates the temperature conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    nomes: list[str] = ['CELSIUS', 'FAHRENHEIT', 'KELVIN']
    display_units(nomes)
    entry_unit, converted_unit = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    converted_t = enums.UnitConverter.convert(input_value, nomes[entry_unit], nomes[converted_unit])
    validate_physical_limits(3, entry_unit, input_value)
    print_conversion(converted_t)


def handle_weight_conversion() -> None:
    """Orchestrates the weight conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    nomes: list[str] = ['KG', 'POUND', 'OUNCE']
    display_units(nomes)
    entry_unit, converted_unit = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    converted_w = enums.UnitConverter.convert(input_value, nomes[entry_unit], nomes[converted_unit])
    validate_physical_limits(3, entry_unit, input_value)
    print_conversion(converted_w)


def handle_length_conversion() -> None:
    """Orchestrates the length conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    nomes: list[str] = ['METER', 'KM', 'MILE']
    display_units(nomes)
    entry_unit, converted_unit = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    converted_l = enums.UnitConverter.convert(input_value, nomes[entry_unit], nomes[converted_unit])
    validate_physical_limits(3, entry_unit, input_value)
    print_conversion(converted_l)


def handle_pressure_conversion() -> None:
    """Orchestrates the pressure conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    nomes: list[str] = ['PASCAL', 'BAR', 'ATM']
    display_units(nomes)
    entry_unit, converted_unit = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    converted_p = enums.UnitConverter.convert(input_value, nomes[entry_unit], nomes[converted_unit])
    validate_physical_limits(3, entry_unit, input_value)
    print_conversion(converted_p)


def validate_physical_limits(category: int, source_unit: int, value: float) -> None:
    """Checks for physical and logical limits and warns the user if exceeded.

    Verifies against Absolute Zero for temperature and non-negativity for
    scalar measures (Length, Weight, Pressure). Also checks for computational
    overflow (infinity).

    Args:
        category: The main menu option (1=Length, 2=Weight, 3=Temp, 4=Pressure).
        source_unit: The ID of the unit being converted from.
        value: The input value to check.
    """
    # 1. Check for Computational Limits (Infinity)
    if math.isinf(value):
        print(
            f'{YELLOW_TEXT}[WARNING] Input is too large for standard calculation '
            f'(Infinite).{RESET}',
        )
        return

    # 2. Check for Physical Limits
    if category == 3:
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
            print(
                f'{YELLOW_TEXT}[WARNING] Physics violation: Value is below Absolute Zero '
                f'({abs_zero_limit}).{RESET}',
            )

    elif category in {1, 2, 4}:  # Length, Weight, Pressure (Scalar units)
        # Generally, these cannot be negative in physical measurement contexts
        if value < 0:
            print(
                f'{YELLOW_TEXT}[WARNING] Physical limitation: '
                f'This measurement usually cannot be negative.{RESET}',
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


def get_valid_number(is_an_entry_number: bool) -> tuple[bool, int]:
    """Gets a valid unit ID from user input.

    Validates that the user input corresponds to an available unit option.

    Returns:
        A tuple containing a validity flag (bool) and the unit ID (int).
    """
    number: int = 0
    try:
        number = int(
            input(
                'Enter the origin unit number: '
                if is_an_entry_number
                else 'Enter the converted unit number: ',
            ),
        )
        if number not in {1, 2, 3}:
            raise exceptions.NotAllowedValueError
    except ValueError:
        print(f'{RED_TEXT}[ERROR] PLEASE ENTER A NUMBER{RESET}')
        is_valid_number = False
    except exceptions.NotAllowedValueError:
        print(f'{RED_TEXT}[ERROR] PLEASE ENTER A VALID NUMBER{RESET}')
        is_valid_number = False
    else:
        is_valid_number = True
    return is_valid_number, number


def main() -> None:
    """Main entry point of the application."""
    print(f'{GREEN_TEXT}Welcome to the CLI Unit Conversor{RESET}')
    while True:
        display_main_menu()
        process_menu_selection()


if __name__ == '__main__':
    main()
