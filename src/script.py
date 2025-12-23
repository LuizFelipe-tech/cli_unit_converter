"""
CLI Unit Converter.

This script provides a command-line interface to convert units between
different systems of measurement, such as length, weight, and temperature.
"""
from __future__ import annotations

DOUBLE_ARROW = "\u2194"


def show_menu() -> None:
  """Displays the main menu options to the standard output.

    Prints the available conversion categories (Length, Weight, Temperature)
    and the exit option.
    """
  print(f"1. Comprimento (Metros {DOUBLE_ARROW} Quilômetros {DOUBLE_ARROW} Milhas")
  print(f"2. Peso (Quilogramas {DOUBLE_ARROW} Libras {DOUBLE_ARROW} Onças)")
  print(f"3. Temperatura (Celsius {DOUBLE_ARROW} Fahrenheit {DOUBLE_ARROW} Kelvin)")
  print("4. Sair")

def select_menu() -> None:
  """Handles the user's menu selection.
    Prompts the user to enter an option number and executes the corresponding logic.
    """
  selected_conversor: int = int(input("Enter the number for the selected option: "))
  match selected_conversor:
    case 3:
      temperature_module()
    case _:
      print("Nothing selected")
def get_temperature_units() -> tuple[int, int]:
  """Prompts the user to select the source and target units for temperature.

    Returns:
        tuple[int, int]: A tuple containing two integers:
            - The first integer represents the source unit ID.
            - The second integer represents the target unit ID.
    """
  print("--- Temperature Conversor selected ---")
  print("Available units below")
  print("1. Fahrenheit")
  print("2. Celsius")
  print("3. Kelvin")
  entry_unit: int = int(input("Enter the origin unit number: "))
  conversion_unit: int = int(input("Enter the converted unit: "))
  return entry_unit, conversion_unit


def convert_temperature(units:tuple[int, int], value_unit:int) -> float:
  """Prompts the user to select the source and target units for temperature.

      Returns:
          tuple[int, int]: A tuple containing two integers:
              - The first integer represents the source unit ID.
              - The second integer represents the target unit ID.
      """
  match units:
    case (1, 2):
      # Fahrenheit to Celsius option
      celsius_t: float = (5 / 9) * (value_unit - 32)
      return celsius_t
    case _:
      return 0.0


def temperature_module() -> None:
  """Orchestrates the temperature conversion workflow.

      This function manages the sequence of getting units, asking for the value,
      performing the conversion, and displaying the result.
      """
  units_chosen: tuple[int, int] = get_temperature_units()
  input_value: int = int(input("Enter the value to be converted: "))
  converted_value: float = convert_temperature(units_chosen, input_value)
  print(f"{converted_value:.2f} degrees celsius")

def main() -> None:
  """Main entry point of the application."""
  show_menu()
  select_menu()


if __name__ == "__main__":
  main()
