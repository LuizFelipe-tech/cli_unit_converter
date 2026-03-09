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
    DATA_STORAGE = auto()

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
