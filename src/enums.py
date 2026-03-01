"""Unit conversion enums and registry logic.

This module defines the physical categories, unit definitions, and the
central UnitConverter class, which manages the conversion between different
units of measurement using a base-unit normalization approach.
"""

from __future__ import annotations

import typing
from enum import Enum, auto
from typing import TYPE_CHECKING, NamedTuple

from loguru import logger

if TYPE_CHECKING:
    from collections.abc import Callable


class Category(Enum):
    """Defines physical categories to prevent invalid cross-category conversions.

    Attributes:
        LENGTH: Length units (base: Meter).
        WEIGHT: Weight/mass units (base: Kilogram).
        TEMPERATURE: Temperature units (base: Celsius).
        PRESSURE: Pressure units (base: Pascal).
        VOLUME: Volume units (base: Liter).
    """

    LENGTH = auto()
    WEIGHT = auto()
    TEMPERATURE = auto()
    PRESSURE = auto()
    VOLUME = auto()

    @property
    def display_name(self) -> str:
        """Returns the human-readable name of the category."""
        return self.name.capitalize()

    @property
    def min_value_base(self) -> float | None:
        """Returns the physical minimum value in the base unit."""
        if self == Category.TEMPERATURE:
            return -273.15
        return 0.0


class UnitDefinition(NamedTuple):
    """Data structure holding metadata and conversion logic for a specific unit.

    Attributes:
        name: The singular name of the unit (e.g., 'Meter').
        plural: The plural name of the unit (e.g., 'Meters').
        category: The physical category the unit belongs to.
        to_base: A callable that converts a value *from* this unit *to* the base unit.
        from_base: A callable that converts a value *from* the base unit *to* this unit.
    """

    name: str
    plural: str
    category: Category
    to_base: Callable[[float], float]
    from_base: Callable[[float], float]


class UnitConverter:
    """Centralizes unit registration and conversion logic using a Base Unit pattern.

    This class acts as a registry and a processor. It normalizes values to a
    base unit (defined per Category) before converting them to the target unit.

    Base units assumed:
        * Length: Meters
        * Weight: Kilograms
        * Temperature: Celsius
        * Pressure: Pascal
        * Volume: Liters

    Attributes:
        registry (dict[str, UnitDefinition]): Internal storage for unit definitions.
    """

    registry: typing.ClassVar[dict[str, UnitDefinition]] = {}

    @classmethod
    def register(cls, key: str, definition: UnitDefinition) -> None:
        """Registers a new unit definition in the central registry.

        Args:
            key (str): The string identifier for the unit (case-insensitive).
            definition (UnitDefinition): The UnitDefinition object containing metadata and formulas.
        """
        cls.registry[key.upper()] = definition
        logger.debug(
            'unit_registered | key={key} category={cat}',
            key=key.upper(),
            cat=definition.category.name,
        )

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Converts a value from one unit to another.

        Args:
            value (float): The numeric value to convert.
            from_unit (str): The string key of the source unit (e.g., 'KM').
            to_unit (str): The string key of the target unit (e.g., 'MILE').

        Returns:
            float: The converted value in the target unit.

        Raises:
            ValueError: If either unit key is not found in the registry.
            TypeError: If the units belong to different physical categories
                (e.g., attempting to convert Length to Weight).
        """
        source = cls.registry.get(from_unit.upper())
        target = cls.registry.get(to_unit.upper())

        if not source or not target:
            logger.error('conversion_failed_unknown_unit | from={f} to={t}', f=from_unit, t=to_unit)
            raise ValueError(f'Unknown unit: {from_unit} or {to_unit}')

        if source.category != target.category:
            logger.error(
                'conversion_failed_category_mismatch | source={src} target={tgt}',
                src=source.category.name,
                tgt=target.category.name,
            )
            raise TypeError(
                f'Invalid conversion: Cannot convert {source.category.name} '
                f'to {target.category.name}.',
            )

        # Step 1: Normalize to base
        value_in_base = source.to_base(value)

        # Step 2: Convert from base to target
        return target.from_base(value_in_base)

    @classmethod
    def get_unit_info(cls, unit_key: str) -> UnitDefinition:
        """Retrieves metadata for a specific unit.

        Args:
            unit_key (str): The string identifier for the unit.

        Returns:
            UnitDefinition: The unit's metadata and conversion functions.

        Raises:
            ValueError: If the provided unit_key is not found in the registry.
        """
        unit = cls.registry.get(unit_key.upper())

        if unit is None:
            logger.error('unit_lookup_failed | unit_key={key}', key=unit_key)
            raise ValueError(f"Unit '{unit_key}' not found in registry.")

        return unit

    @classmethod
    def get_keys_by_category(cls, category: Category) -> list[str]:
        """Returns all registered keys for a given category.

        Args:
            category (Category): The physical category to filter by.

        Returns:
            list[str]: A list of unit keys belonging to the category.
        """
        return [key for key, defn in cls.registry.items() if defn.category == category]


# --- Unit Registration ---

# LENGTH (Base: Meters)
UnitConverter.register(
    'METER',
    UnitDefinition(
        'Meter',
        'Meters',
        Category.LENGTH,
        lambda x: x,  # Already base unit.
        lambda x: x,
    ),
)
UnitConverter.register(
    'KM',
    UnitDefinition(
        'Kilometer',
        'Kilometers',
        Category.LENGTH,
        lambda x: x * 1000.0,  # kilometer -> meter
        lambda x: x / 1000.0,  # meter -> kilometer
    ),
)
UnitConverter.register(
    'MILE',
    UnitDefinition(
        'Mile',
        'Miles',
        Category.LENGTH,
        lambda x: x * 1609.34,  # mile -> meter
        lambda x: x / 1609.34,  # meter -> mile
    ),
)

# WEIGHT (Base: Kilograms)
UnitConverter.register(
    'KG',
    UnitDefinition(
        'Kilogram',
        'Kilograms',
        Category.WEIGHT,
        lambda x: x,  # Already base unit.
        lambda x: x,
    ),
)
UnitConverter.register(
    'POUND',
    UnitDefinition(
        'Pound',
        'Pounds',
        Category.WEIGHT,
        lambda x: x * 0.453592,  # pound -> kilogram
        lambda x: x / 0.453592,  # kilogram -> pound
    ),
)
UnitConverter.register(
    'OUNCE',
    UnitDefinition(
        'Ounce',
        'Ounces',
        Category.WEIGHT,
        lambda x: x * 0.0283495,  # ounce -> kilogram
        lambda x: x / 0.0283495,  # kilogram -> ounce
    ),
)

# TEMPERATURE (Base: Celsius) — uses linear formulas due to non-zero offsets
UnitConverter.register(
    'CELSIUS',
    UnitDefinition(
        'Degree Celsius',
        'Degrees Celsius',
        Category.TEMPERATURE,
        lambda x: x,  # Already base unit.
        lambda x: x,
    ),
)
UnitConverter.register(
    'FAHRENHEIT',
    UnitDefinition(
        'Degree Fahrenheit',
        'Degrees Fahrenheit',
        Category.TEMPERATURE,
        lambda x: (x - 32) * 5 / 9,  # Fahrenheit -> Celsius
        lambda x: (x * 9 / 5) + 32,  # Celsius -> Fahrenheit
    ),
)
UnitConverter.register(
    'KELVIN',
    UnitDefinition(
        'Kelvin',
        'Kelvin',
        Category.TEMPERATURE,
        lambda x: x - 273.15,  # Kelvin -> Celsius
        lambda x: x + 273.15,  # Celsius -> Kelvin
    ),
)

# PRESSURE (Base: Pascal)
UnitConverter.register(
    'PASCAL',
    UnitDefinition(
        'Pascal',
        'Pascals',
        Category.PRESSURE,
        lambda x: x,  # Already base unit.
        lambda x: x,
    ),
)
UnitConverter.register(
    'BAR',
    UnitDefinition(
        'Bar',
        'Bars',
        Category.PRESSURE,
        lambda x: x * 100000.0,  # bar -> Pascal
        lambda x: x / 100000.0,  # Pascal -> bar
    ),
)
UnitConverter.register(
    'ATM',
    UnitDefinition(
        'Atmosphere',
        'Atmospheres',
        Category.PRESSURE,
        lambda x: x * 101325.0,  # atmosphere -> Pascal
        lambda x: x / 101325.0,  # Pascal -> atmosphere
    ),
)

# VOLUME (Base: Liters)
UnitConverter.register(
    'LITER',
    UnitDefinition(
        'Liter',
        'Liters',
        Category.VOLUME,
        lambda x: x,  # Already base unit.
        lambda x: x,
    ),
)
UnitConverter.register(
    'MILLILITER',
    UnitDefinition(
        'Milliliter',
        'Milliliters',
        Category.VOLUME,
        lambda x: x / 1000.0,  # milliliter -> liter
        lambda x: x * 1000.0,  # liter -> milliliter
    ),
)
UnitConverter.register(
    'GALLON_US',
    UnitDefinition(
        'US Gallon',
        'US Gallons',
        Category.VOLUME,
        lambda x: x * 3.78541,  # gallon -> liter
        lambda x: x / 3.78541,  # liter -> gallon
    ),
)
