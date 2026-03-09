import math

import questionary

from config import enums


def print_conversion(converted_value: float, unit_key: str) -> None:
    """Formats and prints the final conversion result using Rich.

    Retrieves the plural name of the target unit from the registry to ensure
    grammatically correct output.

    Args:
        converted_value (float): The numeric result of the conversion.
        unit_key (str): The registry key of the target unit (to fetch its display name).
    """
    unit_plural = enums.UnitConverter.get_unit_info(unit_key).plural
    unit_singular = enums.UnitConverter.get_unit_info(unit_key).name
    questionary.print(
        f'Result: {converted_value:.2f}'
        f' {unit_singular if converted_value in {0, 1} else unit_plural}',
    )


def handle_conversion(category: enums.Category, units_keys: list[str]) -> None:
    """Orchestrates the end-to-end conversion workflow for a given category.

    Guides the user through unit selection, value input, conversion execution,
    physical limit validation, and result display.

    Args:
        category (enums.Category): The category enum member (e.g., Category.LENGTH),
            used to determine specific validation rules (like absolute zero).
        units_keys (list[str]): A list of string keys representing the available units
            in the registry for this category (e.g., ['METER', 'KM']).
    """
    source_unit, target_unit = units_keys
    try:
        input_value: float = float(
            questionary.text('Enter the number to be converted:').ask(),
        )
    except ValueError:
        return

    result = enums.UnitConverter.convert(input_value, source_unit, target_unit)


    validate_physical_limits(category, source_unit, input_value)
    print_conversion(result, target_unit)


def validate_physical_limits(category: enums.Category, unit_key: str, value: float) -> None:
    """Checks for physical/logical limits and warns if exceeded.

    Verifies against Absolute Zero for temperature and non-negativity
    for scalar measures (Length, Weight, Pressure). Guards against
    computational overflow (infinity).

    Args:
        category (enums.Category): The category enum member (e.g., Category.TEMPERATURE).
        unit_key (str): The registry key of the source unit (e.g., 'CELSIUS',
            'FAHRENHEIT'). Used to look up specific physical limits.
        value (float): The input value to validate.
    """
    # Guard against computational overflow
    if math.isinf(value):
        questionary.print(
            '[WARNING] Input is too large for standard calculation (Infinite).[/yellow]',
        )
        return

    # Compare in base units for consistent validation across all unit types
    min_base = category.min_value_base
    if min_base is not None:
        unit_info = enums.UnitConverter.get_unit_info(unit_key)
        value_in_base = unit_info.to_base(value)

        if value_in_base < min_base:
            min_in_unit = unit_info.from_base(min_base)
            # Round for display
            min_in_unit = round(min_in_unit, 2)
            questionary.print(
                f'[WARNING] Physical limitation: Value is below '
                f'minimum possible ({min_in_unit} {unit_info.plural}).',
            )
