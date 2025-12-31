"""CLI Unit Converter.

Converts units of measurement using a command-line interface. Supports conversion
between different systems for length, weight and temperature.
"""

from __future__ import annotations

from collections.abc import Callable
import math
import sys
from typing import TYPE_CHECKING, TypeAlias

import enums
import exceptions

if TYPE_CHECKING:
    from enum import Enum

__version__ = '1.0.0'

BIDIRECTIONAL_ARROW = '\u2194'

RED_TEXT = '\x1b[31m'

GREEN_TEXT = '\x1b[32m'

YELLOW_TEXT = '\033[33m'

RESET = '\x1b[0m'


_ConversionFunc: TypeAlias = Callable[[float], float]


CONVERSION_FACTORS: dict[Enum, _ConversionFunc] = {
    enums.Temperature.FAHRENHEIT_TO_CELSIUS: lambda x: (5 / 9) * (x - 32),
    enums.Temperature.CELSIUS_TO_FAHRENHEIT: lambda x: x * (9 / 5) + 32,
    enums.Temperature.FAHRENHEIT_TO_KELVIN: lambda x: (x - 32) * (5 / 9) + 273.15,
    enums.Temperature.KELVIN_TO_FAHRENHEIT: lambda x: (x - 273.15) * (9 / 5) + 32,
    enums.Temperature.CELSIUS_TO_KELVIN: lambda x: x + 273.15,
    enums.Temperature.KELVIN_TO_CELSIUS: lambda x: x - 273.15,
    enums.Weight.KILOGRAMS_TO_POUNDS: lambda x: x * 2.20462,
    enums.Weight.POUNDS_TO_KILOGRAMS: lambda x: x * 35.274,
    enums.Weight.KILOGRAMS_TO_OUNCES: lambda x: x * 35.274,
    enums.Weight.OUNCES_TO_KILOGRAMS: lambda x: x / 35.274,
    enums.Weight.POUNDS_TO_OUNCES: lambda x: x * 16,
    enums.Weight.OUNCES_TO_POUNDS: lambda x: x / 16,
    enums.Length.METERS_TO_KILOMETERS: lambda x: x / 1000,
    enums.Length.KILOMETERS_TO_METERS: lambda x: x * 1000,
    enums.Length.METERS_TO_MILES: lambda x: x / 1609.34,
    enums.Length.MILES_TO_METERS: lambda x: x * 1609.34,
    enums.Length.KILOMETERS_TO_MILES: lambda x: x / 1.60934,
    enums.Length.MILES_TO_KILOMETERS: lambda x: x * 1.60934,
    enums.Pressure.PASCAL_TO_ATMOSPHERE: lambda x: x / 101325,
    enums.Pressure.ATMOSPHERE_TO_PASCAL: lambda x: x * 101325,
    enums.Pressure.PASCAL_TO_BAR: lambda x: x / 100000,
    enums.Pressure.BAR_TO_PASCAL: lambda x: x * 100000,
    enums.Pressure.ATMOSPHERE_TO_BAR: lambda x: x * 1.01325,
    enums.Pressure.BAR_TO_ATMOSPHERE: lambda x: x / 1.01325,
}

PRINTS: dict[Enum, str] = {}


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
    match valid_option:
        case 1:
            handle_length_conversion()
        case 2:
            handle_weight_conversion()
        case 3:
            handle_temp_conversion()
        case 4:
            handle_pressure_conversion()
        case 5:
            print(f'{YELLOW_TEXT}Exiting the program...{RESET}')
            sys.exit(0)


def display_temp_units() -> None:
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


def print_temp_conversion(units: Enum, converted: float) -> None:
    """Prints the converted temperature.

    Args:
      units: A tuple containing two integers (source_unit, target_unit).
      converted: The numerical result of the conversion.
    """
    match units:
        case enums.Temperature.FAHRENHEIT_TO_CELSIUS:
            print(
                f'{GREEN_TEXT}'
                f'{converted:.2f} {"degrees" if converted != 1 else "degree"} Celsius'
                f'{RESET}',
            )
        case enums.Temperature.CELSIUS_TO_FAHRENHEIT:
            print(
                f'{GREEN_TEXT}'
                f'{converted:.2f} {"degrees" if converted != 1 else "degree"} Fahrenheit'
                f'{RESET}',
            )
        case enums.Temperature.FAHRENHEIT_TO_KELVIN:
            print(f'{converted:.2f} {"Kelvins" if converted != 1 else "Kelvin"}')
        case enums.Temperature.KELVIN_TO_FAHRENHEIT:
            print(
                f'{GREEN_TEXT}'
                f'{converted:.2f} {"degrees" if converted != 1 else "degree"} Fahrenheit'
                f'{RESET}',
            )
        case enums.Temperature.CELSIUS_TO_KELVIN:
            print(
                f'{converted:.2f} {"Kelvins" if converted not in {1, 0} else "Kelvin"}',
            )
        case enums.Temperature.KELVIN_TO_CELSIUS:
            print(
                f'{GREEN_TEXT}'
                f'{converted:.2f} {"degrees" if converted != 1 else "degree"} Celsius'
                f'{RESET}',
            )


def print_weight_conversion(units: tuple[int, int], converted: float) -> None:
    """Prints the converted weight.

    Args:
      units: A tuple containing two integers (source_unit, target_unit).
      converted: The numerical result of the conversion.
    """
    match units:
        case enums.Weight.KILOGRAMS_TO_POUNDS.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Pounds" if converted != 1 else "Pound"}{RESET}')
        case enums.Weight.POUNDS_TO_KILOGRAMS.value:
            print(
                f'{GREEN_TEXT}'
                f'{converted:.2f}{"Kilograms" if converted != 1 else "Kilogram"}{RESET}',
            )
        case enums.Weight.KILOGRAMS_TO_OUNCES.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Ounces" if converted != 1 else "Ounce"}{RESET}')
        case enums.Weight.OUNCES_TO_KILOGRAMS.value:
            print(
                f'{GREEN_TEXT}'
                f'{converted:.2f}{"Kilograms" if converted != 1 else "Kilogram"}{RESET}',
            )
        case enums.Weight.POUNDS_TO_OUNCES.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Ounces" if converted != 1 else "Ounce"}{RESET}')
        case enums.Weight.OUNCES_TO_POUNDS.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Pounds" if converted != 1 else "Pound"}{RESET}')


def print_length_conversion(units: tuple[int, int], converted: float) -> None:
    """Prints the converted length.

    Args:
      units: A tuple containing two integers (source_unit, target_unit).
      converted: The numerical result of the conversion.
    """
    match units:
        case enums.Length.METERS_TO_KILOMETERS.value:
            print(
                f'{GREEN_TEXT}'
                f'{converted:.2f} {"Kilometers" if converted != 1 else "Kilometer"}'
                f'{RESET}',
            )
        case enums.Length.KILOMETERS_TO_METERS.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Meters" if converted != 1 else "Meter"}{RESET}')
        case enums.Length.METERS_TO_MILES.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Miles" if converted != 1 else "Mile"}{RESET}')
        case enums.Length.MILES_TO_METERS.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Meters" if converted != 1 else "Meter"}{RESET}')
        case enums.Length.KILOMETERS_TO_MILES.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Miles" if converted != 1 else "Mile"}{RESET}')
        case enums.Length.MILES_TO_KILOMETERS.value:
            print(
                f'{GREEN_TEXT}'
                f'{converted:.2f} {"Kilometers" if converted != 1 else "Kilometer"}'
                f'{RESET}',
            )


def print_pressure_conversion(units: tuple[int, int], converted: float) -> None:
    """Prints the converted pressure.

    Args:
        units: A tuple containing two integers (source_unit, target_unit).
        converted: The numerical value to be converted.
    """
    match units:
        case enums.Pressure.PASCAL_TO_ATMOSPHERE.value:
            print(
                f'{GREEN_TEXT}'
                f'{converted:.2f} {"Atmospheres" if converted != 1 else "Atmosphere"}'
                f'{RESET}',
            )
        case enums.Pressure.ATMOSPHERE_TO_PASCAL.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Pascals" if converted != 1 else "Pascal"}{RESET}')
        case enums.Pressure.PASCAL_TO_BAR.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Bars" if converted != 1 else "Bar"}{RESET}')
        case enums.Pressure.BAR_TO_PASCAL.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Pascals" if converted != 1 else "Pascal"}{RESET}')
        case enums.Pressure.ATMOSPHERE_TO_BAR.value:
            print(f'{GREEN_TEXT}{converted:.2f} {"Bars" if converted != 1 else "Bar"}{RESET}')
        case enums.Pressure.BAR_TO_ATMOSPHERE.value:
            print(
                f'{GREEN_TEXT}'
                f'{converted:.2f} {"Atmospheres" if converted != 1 else "Atmosphere"}'
                f'{RESET}',
            )


def perform_conversion(units: Enum, value: float) -> float:
    """Generic conversion function handling linear and affine transformations.

    Args:
        units: A tuple (source_unit, target_unit) identifying the conversion.
        value: The numerical value to convert.

    Returns:
        The converted float value.
    """
    conversion_func = CONVERSION_FACTORS[units]
    return conversion_func(value)


def handle_temp_conversion() -> None:
    """Orchestrates the temperature conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    display_temp_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    converted_t = perform_conversion(enums.Temperature(units_chosen), input_value)
    print(converted_t)
    print()
    validate_physical_limits(3, units_chosen[0], input_value)
    print_temp_conversion(enums.Temperature(units_chosen), converted_t)


def handle_weight_conversion() -> None:
    """Orchestrates the weight conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    display_weight_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    converted_w = perform_conversion(enums.Weight(units_chosen), input_value)
    print()
    validate_physical_limits(2, units_chosen[0], input_value)
    print_weight_conversion(units_chosen, converted_w)


def handle_length_conversion() -> None:
    """Orchestrates the length conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    display_length_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    converted_l = perform_conversion(enums.Length(units_chosen), input_value)
    print()
    validate_physical_limits(1, units_chosen[0], input_value)
    print_length_conversion(units_chosen, converted_l)


def handle_pressure_conversion() -> None:
    """Orchestrates the pressure conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    display_pressure_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: float = float(input('Enter the number to be converted: '))
    converted_p = perform_conversion(enums.Pressure(units_chosen), input_value)
    print()
    validate_physical_limits(4, units_chosen[0], input_value)
    print_pressure_conversion(units_chosen, converted_p)


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
