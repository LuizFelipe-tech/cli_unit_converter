"""Unit conversion enums and registry.

Defines physical categories, unit metadata, and the ``UnitConverter``
registry that normalizes values through a base-unit approach.
"""

from __future__ import annotations

from enum import Enum, auto
import typing
from typing import TYPE_CHECKING, NamedTuple

from loguru import logger

if TYPE_CHECKING:
    from collections.abc import Callable


class Category(Enum):
    """Physical categories that prevent invalid cross-category conversions.

    Each member maps to a group of compatible units sharing the same
    dimensional quantity (length, mass, temperature, etc.).
    """

    LENGTH = auto()
    WEIGHT = auto()
    TEMPERATURE = auto()
    PRESSURE = auto()
    VOLUME = auto()

    @property
    def display_name(self) -> str:
        """Returns a human-readable category name."""
        return self.name.capitalize()

    @property
    def min_value_base(self) -> float | None:
        """Returns the physical minimum in base units, or ``None``."""
        if self == Category.TEMPERATURE:
            return -273.15
        return 0.0


class UnitDefinition(NamedTuple):
    """Metadata and conversion lambdas for a single unit.

    Attributes:
        name: Singular display name (e.g., ``'Meter'``).
        plural: Plural display name (e.g., ``'Meters'``).
        category: The physical category this unit belongs to.
        to_base: Converts a value from this unit to the base unit.
        from_base: Converts a value from the base unit to this unit.
    """

    name: str
    plural: str
    category: Category
    to_base: Callable[[float], float]
    from_base: Callable[[float], float]


class UnitConverter:
    """Central registry and processor for unit conversions.

    Normalizes values to a base unit per category before converting
    to the target unit.

    Base units:
        - Length: Meter
        - Weight: Kilogram
        - Temperature: Celsius
        - Pressure: Pascal
        - Volume: Liter
    """

    registry: typing.ClassVar[dict[str, UnitDefinition]] = {}

    @classmethod
    def register(cls, key: str, definition: UnitDefinition) -> None:
        """Registers a unit definition in the registry.

        Args:
            key: Case-insensitive string identifier for the unit.
            definition: ``UnitDefinition`` with metadata and conversion lambdas.
        """
        cls.registry[key.upper()] = definition
        logger.debug(
            'unit_registered | key={k} category={c}',
            k=key.upper(),
            c=definition.category.name,
        )

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Converts a value between two registered units.

        Args:
            value: The numeric value to convert.
            from_unit: Registry key of the source unit.
            to_unit: Registry key of the target unit.

        Returns:
            The converted value in the target unit.

        Raises:
            ValueError: If either unit key is unknown.
            TypeError: If the units belong to different categories.
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
        """Retrieves metadata for a registered unit.

        Args:
            unit_key: The string identifier for the unit.

        Returns:
            The corresponding ``UnitDefinition``.

        Raises:
            ValueError: If the key is not found in the registry.
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
            category: The ``Category`` to filter by.

        Returns:
            A list of unit keys belonging to the category.
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
