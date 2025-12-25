"""CLI Unit Converter.

Converts units of measurement using a command-line interface. Supports conversion
between different systems for length, weight, and temperature.
"""

from __future__ import annotations

import exceptions

DOUBLE_ARROW = '\u2194'


RED_TEXT = '\x1b[31m'


RESET = '\x1b[0m'


def show_menu() -> None:
    """Displays the main menu options to the standard output."""
    print(f'1. Length (Meters {DOUBLE_ARROW} Kilometers {DOUBLE_ARROW} Miles)')
    print(f'2. Weight (Kilograms {DOUBLE_ARROW} Pound {DOUBLE_ARROW} Ounces)')
    print(f'3. Temperature (Celsius {DOUBLE_ARROW} Fahrenheit {DOUBLE_ARROW} Kelvin)')
    print('4. Exit')


def select_menu() -> None:
    """Handles the user's menu selection.

    Prompts the user to enter an option number and executes the corresponding logic.
    """
    while True:
        try:
            selected_conversor: int = int(input("Enter the number for the selected option: "))
            match selected_conversor:
                case 1:
                    length_module()
                case 2:
                    weight_module()
                case 3:
                    temperature_module()
                case _:
                    raise exceptions.NotAllowedValueError  # noqa: TRY301
        except exceptions.NotAllowedValueError:  # type: ignore[misc,unused-ignore]
            print(f"{RED_TEXT}[ERRO] OPÇÃO NÃO EXISTE{RESET}")
        except ValueError:
            print(f"{RED_TEXT}[ERRO] DIGITE UM NÚMERO{RESET}")


def show_temperature_units() -> None:
    """Displays the available units for temperature conversion."""
    print('--- Temperature Converter selected ---')
    print('Available units below')
    print('1. Fahrenheit')
    print('2. Celsius')
    print('3. Kelvin')


def show_weight_units() -> None:
    """Displays the available units for weight conversion."""
    print('--- Weight Converter selected ---')
    print('Available units below')
    print('1. Kilograms')
    print('2. Pounds')
    print('3. Ounces')


# TODO: adicionar cores e TRY method
def show_length_units() -> None:
    """Displays the available units for length conversion."""
    print('--- Length Converter selected ---')
    print('Available units below')
    print('1. Meters')
    print('2. Kilometers')
    print('3. Miles')


def convert_temperature(units: tuple[int, int], value_unit: int) -> float:
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


def convert_weight(units: tuple[int, int], value_unit: int) -> float:
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


def convert_length(units: tuple[int, int], value_unit: int) -> float:
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


def temperature_module() -> None:
    """Orchestrates the temperature conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    show_temperature_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: int = int(input("Enter the value to be converted: "))
    convert_temperature(units_chosen, input_value)


def weight_module() -> None:
    """Orchestrates the weight conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    show_weight_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: int = int(input('Enter the value to be converted: '))
    convert_weight(units_chosen, input_value)


def length_module() -> None:
    """Orchestrates the length conversion workflow.

    Manages the sequence of displaying units, requesting user input for units
    and values, performing the conversion, and displaying the result.
    """
    show_length_units()
    units_chosen: tuple[int, int] = request_units_number()
    input_value: int = int(input('Enter the value to be converted: '))
    convert_length(units_chosen, input_value)


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
    is_valid_number: bool = True
    entry_unit: int = 0
    try:
        entry_unit = int(input('Enter the origin unit number: '))
        if entry_unit in {1, 2, 3}:
            raise exceptions.NotAllowedValueError  # noqa: TRY301
    except ValueError:
        print(f'{RED_TEXT}[ERROR] PLEASE ENTER A NUMBER{RESET}')
        is_valid_number = False
    except exceptions.NotAllowedValueError:
        print(f'{RED_TEXT}[ERROR] PLEASE ENTER A VALID NUMBER{RESET}')
        is_valid_number = False
    return is_valid_number, entry_unit


def get_valid_converted_number() -> tuple[bool, int]:
    """Gets a valid target unit ID from user input.

    Validates that the user input corresponds to an available unit option.

    Returns:
        A tuple containing a validity flag (bool) and the unit ID (int).
    """
    is_converted_number: bool = True
    converted_unit: int = 1
    try:
        converted_unit = int(input('Enter the origin unit number: '))
        if converted_unit in {1, 2, 3}:
            raise exceptions.NotAllowedValueError  # noqa: TRY301
    except ValueError:
        print(f'{RED_TEXT}[ERRO] PLEASE ENTER A NUMBER{RESET}')
        is_converted_number = False
    except exceptions.NotAllowedValueError:
        print(f'{RED_TEXT}[ERRO] PLEASE ENTER A VALID NUMBER{RESET}')
        is_converted_number = False
    return is_converted_number, converted_unit


def main() -> None:
    """Main entry point of the application."""
    show_menu()
    select_menu()


if __name__ == '__main__':
    main()
