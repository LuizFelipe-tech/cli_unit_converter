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
    print(f'1. Comprimento (Metros {DOUBLE_ARROW} Quilômetros {DOUBLE_ARROW} Milhas')
    print(f'2. Peso (Quilogramas {DOUBLE_ARROW} Libras {DOUBLE_ARROW} Onças)')
    print(f'3. Temperatura (Celsius {DOUBLE_ARROW} Fahrenheit {DOUBLE_ARROW} Kelvin)')
    print('4. Sair')


def select_menu() -> None:
    """Handles the user's menu selection.

    Prompts the user to enter an option number and executes the corresponding logic.
    """
    selected_conversor: int = int(input('Enter the number for the selected option: '))
    match selected_conversor:
        case 3:
            temperature_module()
        case _:
            print('Nothing selected')


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


def convert_temperature(units: tuple[int, int], value_unit: int) -> float:
    """Performs temperature conversion based on the selected units and value.

    Returns:
          float: The converted temperature value.
    """
    fahrenheit_t: float = 0.0
    kelvin_t: float = 0.0
    match units:
        case (1, 2):
            # Fahrenheit to Celsius option.
            celsius_t: float = (5 / 9) * (value_unit - 32)
            print(f'{celsius_t:.2f} degrees celsius')
            return celsius_t
        case (2, 1):
            # Celsius to Fahrenheit option.
            fahrenheit_t = value_unit * (9 / 5) + 32
            print(f'{fahrenheit_t:.2f} degrees fahrenheit')
            return fahrenheit_t
        case (1, 3):
            # Fahrenheit to Kelvin.
            kelvin_t = (value_unit - 32) * (5 / 9) + 273.15
            print(f'{kelvin_t:.2f} degrees kelvin')
            return kelvin_t
        case (3, 1):
            # Kelvin to Fahrenheit.
            fahrenheit_t = (value_unit - 273.15) * (9 / 5) + 32
            print(f'{fahrenheit_t:.2f} degrees fahrenheit')
            return fahrenheit_t
        case (2, 3):
            # Celsius to Kelvin.
            kelvin_t = value_unit + 273.15
            print(f'{kelvin_t:.2f} degrees kelvin')
            return kelvin_t
        case (3, 2):
            celsius_t = (value_unit - 273.15) * (9 / 5) + 32
            print(f'{celsius_t:.2f} degrees celsius')
            return celsius_t
        case _:
            return 0.0


def temperature_module() -> None:
    """Orchestrates the temperature conversion workflow.

    This function manages the sequence of getting units, asking for the value,
     performing the conversion, and displaying the result.
    """
    units_chosen: tuple[int, int] = get_temperature_units()
    input_value: int = int(input('Enter the value to be converted: '))
    convert_temperature(units_chosen, input_value)


def main() -> None:
    """Main entry point of the application."""
    show_menu()
    select_menu()


if __name__ == '__main__':
    main()
