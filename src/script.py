"""CLI Unit Converter.

This script provides a command-line interface to convert units between
different systems of measurement, such as length, weight, and temperature.
"""

from __future__ import annotations

DOUBLE_ARROW = '\u2194'


def show_menu() -> None:
    """Displays the main menu options to the standard output.

    Prints the available conversion categories (Length, Weight, Temperature)
    and the exit option.
    """
    print(f'1. Comprimento (Metros {DOUBLE_ARROW} Quilômetros {DOUBLE_ARROW} Milhas)')
    print(f'2. Peso (Quilogramas {DOUBLE_ARROW} Libras {DOUBLE_ARROW} Onças)')
    print(f'3. Temperatura (Celsius {DOUBLE_ARROW} Fahrenheit {DOUBLE_ARROW} Kelvin)')
    print('4. Sair')


def select_menu() -> None:
    """Handles the user's menu selection.

    Prompts the user to enter an option number and executes the corresponding logic.
    """
    selected_conversor: int = int(input('Enter the number for the selected option: '))
    match selected_conversor:
        case 1:
            length_module()
        case 2:
            weight_module()
        case 3:
            temperature_module()
        case _:
            print('Nothing selected')


# TODO: adicionar cores e TRY method
def get_temperature_units() -> tuple[int, int]:
    """Prompts the user to select the source and target units for temperature.

    Returns:
        tuple[int, int]: A tuple containing two integers:
            - The first integer represents the source unit ID.
            - The second integer represents the target unit ID.
    """
    print('--- Temperature Conversor selected ---')
    print('Available units below')
    print('1. Fahrenheit')
    print('2. Celsius')
    print('3. Kelvin')
    entry_unit: int = int(input('Enter the origin unit number: '))
    conversion_unit: int = int(input('Enter the converted unit: '))
    return entry_unit, conversion_unit


# TODO: adicionar cores e TRY method
def get_weight_units() -> tuple[int, int]:
    """Prompts the user to select the source and target units for weight.

    Returns:
        tuple[int, int]: A tuple containing two integers:
            - The first integer represents the source unit ID.
            - The second integer represents the target unit ID.
    """
    print('--- Weight Conversor selected ---')
    print('Available units below')
    print('1. Kilograms')
    print('2. Pounds')
    print('3. Ounces')
    entry_unit: int = int(input('Enter the origin unit number: '))
    conversion_unit: int = int(input('Enter the converted unit: '))
    return entry_unit, conversion_unit


# TODO: adicionar cores e TRY method
def get_length_units() -> tuple[int, int]:
    """Prompts the user to select the source and target units for length.

    Returns:
        tuple[int, int]: A tuple containing two integers:
            - The first integer represents the source unit ID.
            - The second integer represents the target unit ID.
    """
    print('--- Length Conversor selected ---')
    print('Available units below')
    print('1. Meters')
    print('2. Kilometers')
    print('3. Miles')
    entry_unit: int = int(input('Enter the origin unit number: '))
    conversion_unit: int = int(input('Enter the converted unit: '))
    return entry_unit, conversion_unit


def convert_temperature(units: tuple[int, int], value_unit: int) -> float:
    """Performs temperature conversion based on the selected units and value.

    Returns:
          float: The converted temperature value.
    """
    converted_t: float = 0.0
    match units:
        case (1, 2):
            # Fahrenheit to Celsius option.
            converted_t = (5 / 9) * (value_unit - 32)
            print(f'{converted_t:.2f} degrees celsius')
        case (2, 1):
            # Celsius to Fahrenheit option.
            converted_t = value_unit * (9 / 5) + 32
            print(f'{converted_t:.2f} degrees fahrenheit')
        case (1, 3):
            # Fahrenheit to Kelvin.
            converted_t = (value_unit - 32) * (5 / 9) + 273.15
            print(f'{converted_t:.2f} degrees kelvin')
        case (3, 1):
            # Kelvin to Fahrenheit.
            converted_t = (value_unit - 273.15) * (9 / 5) + 32
            print(f'{converted_t:.2f} degrees fahrenheit')
        case (2, 3):
            # Celsius to Kelvin.
            converted_t = value_unit + 273.15
            print(f'{converted_t:.2f} degrees kelvin')
        case (3, 2):
            converted_t = (value_unit - 273.15) * (9 / 5) + 32
            print(f'{converted_t:.2f} degrees celsius')
        case _:
            return 0.0
    return converted_t


def convert_weight(units: tuple[int, int], value_unit: int) -> float:
    """Performs weight conversion based on the selected units and value.

    Returns:
          float: The converted weight value.
    """
    converted_w: float = 0.0
    match units:
        case (1, 2):
            converted_w = value_unit * 2.20462
            print(f'{converted_w:.2f} pounds')
        case (2, 1):
            converted_w = value_unit / 2.20462
            print(f'{converted_w:.2f} kilograms')
        case (1, 3):
            converted_w = value_unit * 35.274
            print(f'{converted_w:.2f} ounces')
        case (3, 1):
            converted_w = value_unit / 35.274
            print(f'{converted_w:.2f} kilograms')
        case (2, 3):
            converted_w = value_unit * 16
            print(f'{converted_w:.2f} ounces')
        case (3, 2):
            converted_w = value_unit / 16
            print(f'{converted_w:.2f} pounds')
    return converted_w


def convert_length(units: tuple[int, int], value_unit: int) -> float:
    """Performs length conversion based on the selected units and value.

    Returns:
          float: The converted length value.
    """
    converted_l: float = 0.0
    match units:
        case (1, 2):
            converted_l = value_unit / 1000
            print(f'{converted_l:.2f} kilometers')
        case (2, 1):
            converted_l = value_unit * 1000
            print(f'{converted_l:.2f} meters')
        case (1, 3):
            converted_l = value_unit / 1609.34
            print(f'{converted_l:.2f} miles')
        case (3, 1):
            converted_l = value_unit * 1609.34
            print(f'{converted_l:.2f} meters')
        case (2, 3):
            converted_l = value_unit / 1.60934
            print(f'{converted_l:.2f} miles')
        case (3, 2):
            converted_l = value_unit * 1.60934
            print(f'{converted_l:.2f} kilometers')
    return converted_l


def temperature_module() -> None:
    """Orchestrates the temperature conversion workflow.

    This function manages the sequence of getting units, asking for the value,
     performing the conversion, and displaying the result.
    """
    units_chosen: tuple[int, int] = get_temperature_units()
    input_value: int = int(input('Enter the value to be converted: '))
    convert_temperature(units_chosen, input_value)


def weight_module() -> None:
    """Orchestrates the weight conversion workflow.

    This function manages the sequence of getting units, asking for the value,
     performing the conversion, and displaying the result.
    """
    units_chosen = get_weight_units()
    input_value: int = int(input('Enter the value to be converted: '))
    convert_weight(units_chosen, input_value)


def length_module() -> None:
    """Orchestrates the length conversion workflow.

    This function manages the sequence of getting units, asking for the value,
     performing the conversion, and displaying the result.
    """
    units_chosen = get_length_units()
    input_value: int = int(input('Enter the value to be converted: '))
    convert_length(units_chosen, input_value)


def main() -> None:
    """Main entry point of the application."""
    show_menu()
    select_menu()


if __name__ == '__main__':
    main()
