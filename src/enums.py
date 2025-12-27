"""An enumeration representing the purpose for which a number is used.

This module defines the `NumberUsedFor` enumeration, which specifies
different contexts in which a number might be utilized. It enables
a clear distinction between the number of usage types within the program.
"""

from __future__ import annotations

from enum import Enum, auto


class NumberUsedFor(Enum):
    """Enumeration defining different purposes for which a number might be used.

    Provides specific categories that can be assigned to numbers to denote their
    use case in different scenarios, such as entry input or conversion unit input.

    Attributes:
        entry_input: Indicates that the number is utilized for entry input purposes.
        conversion_unit_input: Indicates that the number is used for unit
            conversion purposes.
    """

    entry_input = auto()
    conversion_unit_input = auto()


class Length(Enum):
    """Mapeamento de conversões de comprimento.

    Baseado em: 1. Meters, 2. Kilometers, 3. Miles
    """

    METERS_TO_KILOMETERS = (1, 2)
    KILOMETERS_TO_METERS = (2, 1)
    METERS_TO_MILES = (1, 3)
    MILES_TO_METERS = (3, 1)
    KILOMETERS_TO_MILES = (2, 3)
    MILES_TO_KILOMETERS = (3, 2)


class Weight(Enum):
    """Mapeamento de conversões de peso.

    Baseado em: 1. Kilograms, 2. Pounds, 3. Ounces
    """

    KILOGRAMS_TO_POUNDS = (1, 2)
    POUNDS_TO_KILOGRAMS = (2, 1)
    KILOGRAMS_TO_OUNCES = (1, 3)
    OUNCES_TO_KILOGRAMS = (3, 1)
    POUNDS_TO_OUNCES = (2, 3)
    OUNCES_TO_POUNDS = (3, 2)


class Temperature(Enum):
    """Mapeamento de conversões de temperatura.

    Baseado em: 1. Fahrenheit, 2. Celsius, 3. Kelvin
    """

    FAHRENHEIT_TO_CELSIUS = (1, 2)
    CELSIUS_TO_FAHRENHEIT = (2, 1)
    FAHRENHEIT_TO_KELVIN = (1, 3)
    KELVIN_TO_FAHRENHEIT = (3, 1)
    CELSIUS_TO_KELVIN = (2, 3)
    KELVIN_TO_CELSIUS = (3, 2)


class Pressure(Enum):
    """Mapeamento de conversões de pressão.

    Baseado em: 1. Pascal, 2. Atmosphere, 3. Bar
    """

    PASCAL_TO_ATMOSPHERE = (1, 2)
    ATMOSPHERE_TO_PASCAL = (2, 1)
    PASCAL_TO_BAR = (1, 3)
    BAR_TO_PASCAL = (3, 1)
    ATMOSPHERE_TO_BAR = (2, 3)
    BAR_TO_ATMOSPHERE = (3, 2)
