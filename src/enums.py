"""Unit conversion enums and registry logic.

This module defines the physical categories, unit definitions, and the
central UnitConverter class, which manages the conversion between different
units of measurement using a base-unit normalization approach.
"""

from __future__ import annotations

from enum import Enum, auto
import typing
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from collections.abc import Callable


# 1. Physical Categories
class Category(Enum):
    """Defines physical categories to prevent invalid cross-category conversions.

    Attributes:
        LENGTH: Represents length units (base: Meter).
        WEIGHT: Represents weight/mass units (base: Kilogram).
        TEMPERATURE: Represents temperature units (base: Celsius).
        PRESSURE: Represents pressure units (base: Pascal).
    """

    LENGTH = auto()
    WEIGHT = auto()
    TEMPERATURE = auto()
    PRESSURE = auto()

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


# 2. Data Structure for Unit Definitions
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
        * Temperature: Celsius (Chosen due to the complexity of Kelvin/Fahrenheit formulas)
        * Pressure: Pascal

    Attributes:
        registry (dict[str, UnitDefinition]): Internal storage for unit definitions.
    """

    registry: typing.ClassVar[dict[str, UnitDefinition]] = {}

    @classmethod
    def register(cls, key: str, definition: UnitDefinition) -> None:
        """Registers a new unit definition in the central registry.

        Args:
            key: The string identifier for the unit (case-insensitive).
            definition: The UnitDefinition object containing metadata and formulas.
        """
        cls.registry[key.upper()] = definition

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Converts a value from one unit to another.

        Args:
            value: The numeric value to convert.
            from_unit: The string key of the source unit (e.g., 'KM').
            to_unit: The string key of the target unit (e.g., 'MILE').

        Returns:
            float: The converted value in the target unit.

        Raises:
            ValueError: If either unit key is not found in the registry.
            TypeError: If the units belong to different physical categories
                (e.g., attempting to convert Length to Weight).
        """
        source = cls.registry.get(from_unit.upper())
        target = cls.registry.get(to_unit.upper())

        # Safety Validations (Logic and Consistency)
        if not source or not target:
            raise ValueError(f'Unknown unit: {from_unit} or {to_unit}')

        if source.category != target.category:
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
            unit_key: The string identifier for the unit.

        Returns:
            UnitDefinition: The unit details the object.

        Raises:
            ValueError: If the provided unit_key is not found in the registry.
        """
        unit = cls.registry.get(unit_key.upper())

        if unit is None:
            raise ValueError(f"Unit '{unit_key}' not found in registry.")

        return unit

    @classmethod
    def get_keys_by_category(cls, category: Category) -> list[str]:
        """Returns all registered keys for a given category.

        Args:
            category: The physical category to filter by.

        Returns:
            list[str]: A list of unit keys belonging to the category.
        """
        return [key for key, defn in cls.registry.items() if defn.category == category]


# --- Unit Configuration (Registration of supported units) ---

# LENGTH CATEGORY (Base Unit: Meters)
# All length units are registered with their conversion factors to and from Meters.
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

# WEIGHT CATEGORY (Base Unit: Kilograms)
# All weight units are registered with their conversion factors to and from Kilograms.
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

# TEMPERATURE CATEGORY (Base Unit: Celsius)
# Temperature requires linear formulas (y = ax + b) due to non-zero offsets.
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

# PRESSURE CATEGORY (Base Unit: Pascal)
# All pressure units are registered with their conversion factors to and from Pascals.
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
