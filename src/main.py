"""CLI Unit Converter.

Converts units of measurement using a command-line interface. Supports conversion
between different systems for length, weight, and temperature.
"""

from __future__ import annotations

import sys

import exceptions

BIDIRECTIONAL_ARROW = '\u2194'

RED_TEXT = '\x1b[31m'

GREEN_TEXT = '\x1b[32m'

YELLOW_TEXT = '\033[33m'

RESET = '\x1b[0m'


def display_main_menu() -> None:
    """Displays the main menu options to the standard output."""
    print(f'1. Length (Meters {BIDIRECTIONAL_ARROW} Kilometers {BIDIRECTIONAL_ARROW} Miles)')
    print(f'2. Weight (Kilograms {BIDIRECTIONAL_ARROW} Pound {BIDIRECTIONAL_ARROW} Ounces)')
    print(f'3. Temperature (Celsius {BIDIRECTIONAL_ARROW} Fahrenheit {BIDIRECTIONAL_ARROW} Kelvin)')
    print('4. Exit')


def process_menu_selection() -> None:
    """Processes the menu selection.

    Asks for an option number and runs the corresponding conversion logic. Handles
    invalid inputs internally by catching exceptions and printing error messages.
    """
    while True:
        try:
            selected_option: int = int(input('Enter the number for the selected option: '))
            if selected_option not in {1, 2, 3, 4}:
                raise exceptions.NotAllowedValueError
        except exceptions.NotAllowedValueError:  # type: ignore[misc,unused-ignore]  # noqa: PERF203
            print(f'{RED_TEXT}[ERROR] PLEASE ENTER A VALID NUMBER{RESET}')
        except ValueError:
            print(f'{RED_TEXT}[ERROR] PLEASE ENTER A NUMBER{RESET}')
        else:
            break
    match selected_option:
        case 1:
            handle_length_conversion()
        case 2:
            handle_weight_conversion()
        case 3:
            handle_temperature_conversion()
        case 4:
            print(f'{YELLOW_TEXT}Exiting the program...{RESET}')
            sys.exit(0)


def display_temperature_units() -> None:
    """Displays the available units for temperature conversion."""
    print()
    print(f'{GREEN_TEXT}--- Temperature Converter selected ---{RESET}')
    print('Available units below')
    print('1. Fahrenheit')
    print('2. Celsius')
    print('3. Kelvin')


def display_weight_units() -> None:
    """Displays the available units for weight conversion."""
    print()
    print(f'{GREEN_TEXT}--- Weight Converter selected ---{RESET}')
    print('Available units below')
    print('1. Kilograms')
    print('2. Pounds')
    print('3. Ounces')


def display_length_units() -> None:
    """Displays the available units for length conversion."""
    print()
    print(f'{GREEN_TEXT}--- Length Converter selected ---{RESET}')
    print('Available units below')
    print('1. Meters')
    print('2. Kilometers')
    print('3. Miles')


def temperature_conversion(units: tuple[int, int], value_unit: int) -> float:
    """Performs temperature conversion based on the selected units and value.

    Args:
      units: A tuple containing two integers (source_unit, target_unit).
      value_unit: The numerical value to be converted.

    Returns:
      The converted temperature value as a float. Returns 0.0 if the unit
      combination is not matched.
    """
    converted_t: float = 0.0
    match units:
        case (1, 2):
            # Fahrenheit to Celsius option.
            converted_t = (5 / 9) * (value_unit - 32)
            print(f'{converted_t:.2f} degrees Celsius')
        case (2, 1):
            # Celsius to Fahrenheit option.
            converted_t = value_unit * (9 / 5) + 32
            print(f'{converted_t:.2f} degrees Fahrenheit')
        case (1, 3):
            # Fahrenheit to Kelvin.
            converted_t = (value_unit - 32) * (5 / 9) + 273.15
            print(f'{converted_t:.2f} Kelvin')
        case (3, 1):
            # Kelvin to Fahrenheit.
            converted_t = (value_unit - 273.15) * (9 / 5) + 32
            print(f'{converted_t:.2f} degrees Fahrenheit')
        case (2, 3):
            # Celsius to Kelvin.
            converted_t = value_unit + 273.15
            print(f'{converted_t:.2f} Kelvin')
        case (3, 2):
            converted_t = (value_unit - 273.15) * (9 / 5) + 32
            print(f'{converted_t:.2f} degrees Celsius')
        case _:
            return 0.0
    return converted_t


def weight_conversion(units: tuple[int, int], value_unit: int) -> float:
    """Performs weight conversion based on the selected units and value.

    Args:
      units: A tuple containing two integers (source_unit, target_unit).
      value_unit: The numerical value to be converted.

    Returns:
      The converted weight value as a float. Returns 0.0 if the unit
      combination is not matched.
    """
    converted_w: float = 0.0
    match units:
        case (1, 2):
            converted_w = value_unit * 2.20462
            print(f'{converted_w:.2f} Pounds')
        case (2, 1):
            converted_w = value_unit / 2.20462
            print(f'{converted_w:.2f} Kilograms')
        case (1, 3):
            converted_w = value_unit * 35.274
            print(f'{converted_w:.2f} Ounces')
        case (3, 1):
            converted_w = value_unit / 35.274
            print(f'{converted_w:.2f} Kilograms')
        case (2, 3):
            converted_w = value_unit * 16
            print(f'{converted_w:.2f} Ounces')
        case (3, 2):
            converted_w = value_unit / 16
            print(f'{converted_w:.2f} Pounds')
    return converted_w


def length_conversion(units: tuple[int, int], value_unit: int) -> float:
    """Performs length conversion based on the selected units and value.

    Args:
      units: A tuple containing two integers (source_unit, target_unit).
      value_unit: The numerical value to be converted.

    Returns:
      The converted length value as a float. Returns 0.0 if the unit
      combination is not matched.
    """
    converted_l: float = 0.0
    match units:
        case (1, 2):
            converted_l = value_unit / 1000
            print(f'{converted_l:.2f} Kilometers')
        case (2, 1):
            converted_l = value_unit * 1000
            print(f'{converted_l:.2f} Meters')
        case (1, 3):
            converted_l = value_unit / 1609.34
            print(f'{converted_l:.2f} Miles')
        case (3, 1):
            converted_l = value_unit * 1609.34
            print(f'{converted_l:.2f} Meters')
        case (2, 3):
            converted_l = value_unit / 1.60934
            print(f'{converted_l:.2f} Miles')
        case (3, 2):
            converted_l = value_unit * 1.60934
            print(f'{converted_l:.2f} Kilometers')
    return converted_l


def handle_temperature_conversion() -> None:
    """Orchestrates the temperature conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    display_temperature_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: int = int(input('Enter the number to be converted: '))
    temperature_conversion(units_chosen, input_value)


def handle_weight_conversion() -> None:
    """Orchestrates the weight conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    display_weight_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: int = int(input('Enter the number to be converted: '))
    weight_conversion(units_chosen, input_value)


def handle_length_conversion() -> None:
    """Orchestrates the length conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    display_length_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: int = int(input('Enter the number to be converted: '))
    length_conversion(units_chosen, input_value)


def request_units_number() -> tuple[int, int]:
    """Requests the source and target unit numbers from the user.

    Loops until valid inputs are received for both the entry unit and the
    target unit.

    Returns:
      A tuple containing two integers: (valid_entry_number, valid_converted_number).
    """
    while True:
        is_valid_number, valid_entry_number = get_valid_entry_number()
        if is_valid_number:
            break
        continue
    while True:
        is_valid_number, valid_converted_number = get_valid_converted_number()
        if is_valid_number:
            break
        continue
    return valid_entry_number, valid_converted_number


def get_valid_entry_number() -> tuple[bool, int]:
    """Gets a valid source unit ID from user input.

    Validates that the user input corresponds to an available unit option.

    Returns:
        A tuple containing a validity flag (bool) and the unit ID (int).
    """
    entry_unit: int = 0
    try:
        entry_unit = int(input('Enter the origin unit number: '))
        if entry_unit not in {1, 2, 3}:
            raise exceptions.NotAllowedValueError
    except ValueError:
        print(f'{RED_TEXT}[ERROR] PLEASE ENTER A NUMBER{RESET}')
        is_valid_number = False
    except exceptions.NotAllowedValueError:
        print(f'{RED_TEXT}[ERROR] PLEASE ENTER A VALID NUMBER{RESET}')
        is_valid_number = False
    else:
        is_valid_number = True
    return is_valid_number, entry_unit


def get_valid_converted_number() -> tuple[bool, int]:
    """Gets a valid target unit ID from user input.

    Validates that the user input corresponds to an available unit option.

    Returns:
        A tuple containing a validity flag (bool) and the unit ID (int).
    """
    converted_unit: int = 1
    try:
        converted_unit = int(input('Enter the converted unit number: '))
        if converted_unit not in {1, 2, 3}:
            raise exceptions.NotAllowedValueError
    except ValueError:
        print(f'{RED_TEXT}[ERRO] PLEASE ENTER A NUMBER{RESET}')
        is_valid_number = False
    except exceptions.NotAllowedValueError:
        print(f'{RED_TEXT}[ERRO] PLEASE ENTER A VALID NUMBER{RESET}')
        is_valid_number = False
    else:
        is_valid_number = True
    return is_valid_number, converted_unit


def main() -> None:
    """Main entry point of the application."""
    print()
    print(f'{GREEN_TEXT}Welcome to the CLI Unit Conversor{RESET}')
    display_main_menu()
    process_menu_selection()


if __name__ == '__main__':
    while True:
        main()
