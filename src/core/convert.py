"""Conversion orchestration and result display.

Handles user input, delegates to the conversion registry, validates
physical limits, and prints the formatted result.
"""

from __future__ import annotations

import math

from loguru import logger
import questionary

from config import enums


def print_conversion(converted_value: float, unit_key: str) -> None:
    """Formats and displays the conversion result.

    Chooses singular or plural unit name based on the numeric value.

    Args:
        converted_value: The numeric result of the conversion.
        unit_key: Registry key of the target unit.
    """
    info = enums.UnitConverter.get_unit_info(unit_key)
    label = info.name if converted_value in {0, 1} else info.plural
    questionary.print(
        f'Result: {converted_value:.2f} {label}',
        style='bold fg:cyan',
    )


def handle_conversion(category: enums.Category, units_keys: list[str]) -> None:
    """Orchestrates the full conversion workflow.

    Prompts for a numeric value, converts between the selected units,
    validates physical limits, and displays the result.

    Args:
        category: The physical category (e.g., ``Category.LENGTH``).
        units_keys: Two-element list ``[source_key, target_key]``.
    """
    source_unit, target_unit = units_keys
    logger.debug(
        'conversion_start | source={src} target={tgt}',
        src=source_unit,
        tgt=target_unit,
    )

    try:
        raw = questionary.text('Enter the value to convert:').ask()
        input_value: float = float(raw)
    except (ValueError, TypeError):
        logger.warning('invalid_input | raw={raw}', raw=raw)
        questionary.print('Invalid input. Please enter a numeric value.', style='bold fg:red')
        return

    result = enums.UnitConverter.convert(input_value, source_unit, target_unit)
    logger.info(
        'conversion_ok | value={val} from={src} to={tgt} result={res}',
        val=input_value,
        src=source_unit,
        tgt=target_unit,
        res=result,
    )

    validate_physical_limits(category, source_unit, input_value)
    print_conversion(result, target_unit)


def validate_physical_limits(
    category: enums.Category,
    unit_key: str,
    value: float,
) -> None:
    """Warns when a value exceeds known physical boundaries.

    Checks for computational overflow (infinity) and compares the
    value against the category's minimum in base units (e.g., absolute
    zero for temperature, zero for scalar measures).

    Args:
        category: The physical category being validated.
        unit_key: Registry key of the source unit.
        value: The raw input value to validate.
    """
    # Guard: computational overflow
    if math.isinf(value):
        logger.warning('overflow_detected | value=inf')
        questionary.print(
            'Warning: Input is too large for standard calculation (infinite).',
            style='bold fg:yellow',
        )
        return

    # Validate against the category minimum in base units
    min_base = category.min_value_base
    if min_base is not None:
        unit_info = enums.UnitConverter.get_unit_info(unit_key)
        value_in_base = unit_info.to_base(value)

        if value_in_base < min_base:
            min_in_unit = round(unit_info.from_base(min_base), 2)
            logger.warning(
                'below_physical_min | value_base={vb} min_base={mb}',
                vb=value_in_base,
                mb=min_base,
            )
            questionary.print(
                f'Warning: Value is below the physical minimum ({min_in_unit} {unit_info.plural}).',
                style='bold fg:yellow',
            )
