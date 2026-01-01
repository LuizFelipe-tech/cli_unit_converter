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


# 2. Data Structure for Unit Definitions
class UnitDefinition(NamedTuple):
    """Data structure holding metadata and conversion logic for a specific unit.

    Attributes:
        id: A unique numeric identifier for the unit.
        name: The singular name of the unit (e.g., 'Meter').
        plural: The plural name of the unit (e.g., 'Meters').
        category: The physical category the unit belongs to.
        to_base: A callable that converts a value *from* this unit *to* the base unit.
        from_base: A callable that converts a value *from* the base unit *to* this unit.
    """

    id: int
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
        _registry (dict[str, UnitDefinition]): Internal storage for unit definitions.
    """

    _registry: typing.ClassVar[dict[str, UnitDefinition]] = {}

    @classmethod
    def register(cls, key: str, definition: UnitDefinition) -> None:
        """Registers a new unit definition in the central registry.

        Args:
            key: The string identifier for the unit (case-insensitive).
            definition: The UnitDefinition object containing metadata and formulas.
        """
        cls._registry[key.upper()] = definition

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
        source = cls._registry.get(from_unit.upper())
        target = cls._registry.get(to_unit.upper())

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
    def get_unit_info(cls, unit_key: str) -> UnitDefinition | None:
        """Retrieves metadata for a specific unit.

        Args:
            unit_key: The string identifier for the unit.

        Returns:
            UnitDefinition | None: The unit details if found, otherwise None.
        """
        return cls._registry.get(unit_key.upper())


# --- Unit Configuration (Where the magic happens) ---

# LENGTH (Base: Meters)
UnitConverter.register(
    'METER',
    UnitDefinition(
        1,
        'Meter',
        'Meters',
        Category.LENGTH,
        lambda x: x,  # Already base
        lambda x: x,
    ),
)
UnitConverter.register(
    'KM',
    UnitDefinition(
        2,
        'Kilometer',
        'Kilometers',
        Category.LENGTH,
        lambda x: x * 1000.0,  # km -> m
        lambda x: x / 1000.0,  # m -> km
    ),
)
UnitConverter.register(
    'MILE',
    UnitDefinition(
        3,
        'Mile',
        'Miles',
        Category.LENGTH,
        lambda x: x * 1609.34,  # mile -> m
        lambda x: x / 1609.34,  # m -> mile
    ),
)

# WEIGHT (Base: Kilograms)
UnitConverter.register(
    'KG',
    UnitDefinition(
        1,
        'Kilogram',
        'Kilograms',
        Category.WEIGHT,
        lambda x: x,
        lambda x: x,
    ),
)
UnitConverter.register(
    'POUND',
    UnitDefinition(
        2,
        'Pound',
        'Pounds',
        Category.WEIGHT,
        lambda x: x * 0.453592,  # lb -> kg
        lambda x: x / 0.453592,  # kg -> lb
    ),
)
UnitConverter.register(
    'OUNCE',
    UnitDefinition(
        3,
        'Ounce',
        'Ounces',
        Category.WEIGHT,
        lambda x: x * 0.0283495,  # oz -> kg
        lambda x: x / 0.0283495,  # kg -> oz
    ),
)

# TEMPERATURE (Base: Celsius)
# Note: Temperature requires linear formulas (y = ax + b), not just a multiplier factor.
UnitConverter.register(
    'CELSIUS',
    UnitDefinition(
        1,
        'Degree Celsius',
        'Degrees Celsius',
        Category.TEMPERATURE,
        lambda x: x,
        lambda x: x,
    ),
)
UnitConverter.register(
    'FAHRENHEIT',
    UnitDefinition(
        2,
        'Degree Fahrenheit',
        'Degrees Fahrenheit',
        Category.TEMPERATURE,
        lambda x: (x - 32) * 5 / 9,  # F -> C
        lambda x: (x * 9 / 5) + 32,  # C -> F
    ),
)
UnitConverter.register(
    'KELVIN',
    UnitDefinition(
        3,
        'Kelvin',
        'Kelvin',
        Category.TEMPERATURE,
        lambda x: x - 273.15,  # K -> C
        lambda x: x + 273.15,  # C -> K
    ),
)

# PRESSURE (Base: Pascal)
UnitConverter.register(
    'PASCAL',
    UnitDefinition(
        1,
        'Pascal',
        'Pascals',
        Category.PRESSURE,
        lambda x: x,
        lambda x: x,
    ),
)
UnitConverter.register(
    'BAR',
    UnitDefinition(
        2,
        'Bar',
        'Bars',
        Category.PRESSURE,
        lambda x: x * 100000.0,  # bar -> Pa
        lambda x: x / 100000.0,  # Pa -> bar
    ),
)
UnitConverter.register(
    'ATM',
    UnitDefinition(
        3,
        'Atmosphere',
        'Atmospheres',
        Category.PRESSURE,
        lambda x: x * 101325.0,  # atm -> Pa
        lambda x: x / 101325.0,  # Pa -> atm
    ),
)
