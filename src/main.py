"""CLI Unit Converter.

Converts units of measurement using a command-line interface. Supports conversion
between different systems for length, weight and temperature.
"""

from __future__ import annotations

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
        except exceptions.NotAllowedValueError:  # type: ignore[misc,unused-ignore]  # noqa: PERF203
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
    match valid_option:
        case 1:
            handle_length_conversion()
        case 2:
            handle_weight_conversion()
        case 3:
            handle_temperature_conversion()
        case 4:
            handle_pressure_conversion()
        case 5:
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


def display_pressure_units() -> None:
    """Displays the available units for pressure conversion."""
    print()
    print(f'{GREEN_TEXT}--- Pressure Converter selected ---{RESET}')
    print('Available units below')
    print('1. Pascal')
    print('2. Atmosphere')
    print('3. Bar')


def temperature_conversion(units: tuple[int, int], value_unit: float) -> float:
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
            print(f'{converted_t:.2f} {"degrees" if converted_t != 1 else "degree"} Celsius')
        case (2, 1):
            # Celsius to Fahrenheit option.
            converted_t = value_unit * (9 / 5) + 32
            print(f'{converted_t:.2f} {"degrees" if converted_t != 1 else "degree"} Fahrenheit')
        case (1, 3):
            # Fahrenheit to Kelvin.
            converted_t = (value_unit - 32) * (5 / 9) + 273.15
            print(f'{converted_t:.2f} {"Kelvins" if converted_t != 1 else "Kelvin"}')
        case (3, 1):
            # Kelvin to Fahrenheit.
            converted_t = (value_unit - 273.15) * (9 / 5) + 32
            print(
                f'{converted_t:.2f} {"Kelvins" if converted_t not in {1, 0} else "Kelvin"}',
            )
        case (2, 3):
            # Celsius to Kelvin.
            converted_t = value_unit + 273.15
            print(
                f'{converted_t:.2f} {"Kelvins" if converted_t not in {1, 0} else "Kelvin"}',
            )
        case (3, 2):
            # Kelvin to Celsius.
            converted_t = value_unit - 273.15
            print(f'{converted_t:.2f} {"degrees" if converted_t != 1 else "degree"} Celsius')
        case _:
            return 0.0
    return converted_t


def weight_conversion(units: tuple[int, int], value_unit: float) -> float:
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


def length_conversion(units: tuple[int, int], value_unit: float) -> float:
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


def pressure_conversion(units: tuple[int, int], value_unit: float) -> float:
    """Performs pressure conversion based on the selected units and value.

    Args:
      units: A tuple containing two integers (source_unit, target_unit).
      value_unit: The numerical value to be converted.

    Returns:
      The converted pressure value as a float. Returns 0.0 if the unit
      combination is not matched.
    """
    converted_p: float = 0.0
    match units:
        case (1, 2):
            # Pascal to Atmosphere
            converted_p = value_unit / 101325
            print(f'{converted_p:.2f} Atmosphere')
        case (2, 1):
            # Atmosphere to Pascal
            converted_p = value_unit * 101325
            print(f'{converted_p:.2f} Pascal')
        case (1, 3):
            # Pascal to Bar
            converted_p = value_unit / 100000
            print(f'{converted_p:.2f} Bar')
        case (3, 1):
            # Bar to Pascal
            converted_p = value_unit * 100000
            print(f'{converted_p:.2f} Pascal')
        case (2, 3):
            # Atmosphere to Bar
            converted_p = value_unit * 1.01325
            print(f'{converted_p:.2f} Bar')
        case (3, 2):
            # Bar to Atmosphere
            converted_p = value_unit * 0.98692
            print(f'{converted_p:.2f} Atmosphere')
    return converted_p


def handle_temperature_conversion() -> None:
    """Orchestrates the temperature conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    display_temperature_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    temperature_conversion(units_chosen, input_value)


def handle_weight_conversion() -> None:
    """Orchestrates the weight conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    display_weight_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    weight_conversion(units_chosen, input_value)


def handle_length_conversion() -> None:
    """Orchestrates the length conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    display_length_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    length_conversion(units_chosen, input_value)


def handle_pressure_conversion() -> None:
    """Orchestrates the pressure conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    display_pressure_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    pressure_conversion(units_chosen, input_value)


def request_units_number() -> tuple[int, int]:
    """Requests the source and target unit numbers from the user.

    Loops until valid inputs are received for both the entry unit and the
    target unit.

    Returns:
      A tuple containing two integers: (valid_entry_number, valid_converted_number).
    """
    while True:
        is_valid_number, valid_entry_number = get_valid_number(enums.NumberUsedFor(1))
        if is_valid_number:
            break
        continue
    while True:
        is_valid_number, valid_converted_number = get_valid_number(enums.NumberUsedFor(2))
        if is_valid_number:
            break
        continue
    return valid_entry_number, valid_converted_number


def get_valid_number(unit_indicator: enums.NumberUsedFor) -> tuple[bool, int]:
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
                if unit_indicator == enums.NumberUsedFor.entry_input
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
