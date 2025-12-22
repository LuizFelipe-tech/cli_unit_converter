"""
CLI Unit Converter
"""
from __future__ import annotations

DOUBLE_ARROW = "\u2194"


def exibir_menu() -> None:
  """Shows menu"""
  print(f"1. Comprimento (Metros {DOUBLE_ARROW} Quilômetros {DOUBLE_ARROW} Milhas")
  print(f"2. Peso (Quilogramas {DOUBLE_ARROW} Libras {DOUBLE_ARROW} Onças)")
  print(f"3. Temperatura (Celsius {DOUBLE_ARROW} Fahrenheit {DOUBLE_ARROW} Kelvin)")
  print("4. Sair")


def select_units() -> tuple[int, int]:
  """Get the target units from the user"""
  print("--- Temperature Conversor selected ---")
  print("Available units below")
  print("1. Fahrenheit")
  print("2. Celsius")
  print("3. Kelvin")
  entry_unit: int = int(input("Enter the origin unit number: "))
  conversion_unit: int = int(input("Enter the converted unit: "))
  return entry_unit, conversion_unit


def units_conversor(units, value_unit) -> float:
  """Convert to the desired units"""
  match units:
    case (1, 2):
      # Fahrenheit to Celsius option
      celsius_t: float = (5 / 9) * (value_unit - 32)
      return celsius_t
  return 0.0


def main() -> None:
  """" Main Function """
  exibir_menu()
  selected_conversor: int = int(input("Enter the number for the selected option"))
  selected_units: tuple[int, int] = select_units()
  value: int = int(input("Enter the value to be converted: "))
  converted: float = units_conversor(selected_units, value)
  print(f"{converted:.2f} degrees celsius")


if __name__ == "__main__":
  main()
