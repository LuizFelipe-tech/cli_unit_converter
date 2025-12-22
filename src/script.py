"""
CLI Unit Converter
"""
from __future__ import annotations

DOUBLE_ARROW = "\u2194"

def exibir_menu() -> None:
  """"Shows menu"""
  print(f"1. Comprimento (Metros {DOUBLE_ARROW} Quilômetros {DOUBLE_ARROW} Milhas")
  print(f"2. Peso (Quilogramas {DOUBLE_ARROW} Libras {DOUBLE_ARROW} Onças)")
  print(f"3. Temperatura (Celsius {DOUBLE_ARROW} Fahrenheit {DOUBLE_ARROW} Kelvin)")
  print("4. Sair")

def select_units() -> tuple[str, str]:
  """Get the target units from the user"""
  entry_unit: str = input("Digite a unidade de origem: ")
  conversion_unit: str = input("Digite a unidade de conversão: ")
  return entry_unit, conversion_unit


def units_conversor(units) -> None:
  """Convert to the desired units"""
  match units:
    case ("Fahrenheit", "Celsius")

def main() -> None:
  """" Main Function """
  exibir_menu()
  selected_units: tuple[str, str] = select_units()
  units_conversor(selected_units)

if __name__ == "__main__":
    main()
