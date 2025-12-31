"""An enumeration representing the purpose for which a number is used.

This module defines the `NumberUsedFor` enumeration, which specifies
different contexts in which a number might be utilized. It enables
a clear distinction between the number of usage types within the program.
"""

from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

# We use typing_extensions for compatibility with older Python versions
# if you are on Python 3.11+, you can import Self from typing directly.
from typing_extensions import Self

if TYPE_CHECKING:
    from collections.abc import Callable


class NumberUsedFor(Enum):
    """Defines the different contexts in which a number might be used.

    Provides specific categories that can be assigned to numbers to denote their
    use case in different scenarios, ensuring type safety and clarity.

    Attributes:
        entry_input: Indicates that the number is utilized for direct entry input.
        conversion_unit_input: Indicates that the number is used specifically
            for unit conversion purposes.
    """

    entry_input = auto()
    conversion_unit_input = auto()


class RichConversionEnum(Enum):
    """Base enumeration class for unit conversions with rich metadata.

    This class extends the standard Enum to support embedded conversion logic
    (lambda functions) and string formatting (singular/plural labels).
    Specific unit categories (e.g., Length, Weight) extend this class.

    Attributes:
        conversion_func (Callable[[float], float]): The function that performs
            the mathematical conversion.
        label_singular (str): The label to use when the value is 1 (e.g., “Meter”).
        label_plural (str): The label to use when the value is not 1 (e.g., “Meters”).
    """

    conversion_func: Callable[[float], float]
    label_singular: str
    label_plural: str

    def __new__(
        cls,
        source: int,
        target: int,
        func: Callable[[float], float],
        singular: str,
        plural: str,
    ) -> Self:
        """Creates a new instance of the RichConversionEnum.

        Args:
            source (int): The unique identifier for the source unit.
            target (int): The unique identifier for the target unit.
            func (Callable[[float], float]): A lambda or function that takes a
                float value and returns the converted float value.
            singular (str): The display name for a singular unit value.
            plural (str): The display name for a plural unit value.

        Returns:
            Self: The created enumeration member instance.
        """
        obj = object.__new__(cls)
        obj._value_ = (source, target)
        obj.conversion_func = func
        obj.label_singular = singular
        obj.label_plural = plural
        return obj

    def convert(self, value: float) -> float:
        """Performs the unit conversion on the given value.

        Args:
            value (float): The numerical value to convert.

        Returns:
            float: The converted value based on the stored conversion function.
        """
        return self.conversion_func(value)

    def format_text(self, value: float) -> str:
        """Formats the value with the appropriate unit label.

        Args:
            value (float): The numerical value to format.

        Returns:
            str: A formatted string (e.g., “1.00 Meter” or "2.50 Meters”).
        """
        name = self.label_singular if value in {1, -1} else self.label_plural
        return f'{value:.2f} {name}'


class Length(RichConversionEnum):
    """Mapping of length unit conversions.

    IDs:
        1: Meters
        2: Kilometers
        3: Miles
    """

    METERS_TO_KILOMETERS = (1, 2, lambda x: x / 1000.0, 'Kilometer', 'Kilometers')
    KILOMETERS_TO_METERS = (2, 1, lambda x: x * 1000.0, 'Meter', 'Meters')

    METERS_TO_MILES = (1, 3, lambda x: x * 0.000621371, 'Mile', 'Miles')
    MILES_TO_METERS = (3, 1, lambda x: x / 0.000621371, 'Meter', 'Meters')
    KILOMETERS_TO_MILES = (2, 3, lambda x: x * 0.621371, 'Mile', 'Miles')
    MILES_TO_KILOMETERS = (3, 2, lambda x: x / 0.621371, 'Kilometer', 'Kilometers')


class Weight(RichConversionEnum):
    """Mapping of weight unit conversions.

    IDs:
        1: Kilograms
        2: Pounds
        3: Ounces
    """

    KILOGRAMS_TO_POUNDS = (1, 2, lambda x: x * 2.20462, 'Pound', 'Pounds')
    POUNDS_TO_KILOGRAMS = (2, 1, lambda x: x / 2.20462, 'Kilogram', 'Kilograms')
    KILOGRAMS_TO_OUNCES = (1, 3, lambda x: x * 35.274, 'Ounce', 'Ounces')
    OUNCES_TO_KILOGRAMS = (3, 1, lambda x: x / 35.274, 'Kilogram', 'Kilograms')
    POUNDS_TO_OUNCES = (2, 3, lambda x: x * 16.0, 'Ounce', 'Ounces')
    OUNCES_TO_POUNDS = (3, 2, lambda x: x / 16.0, 'Pound', 'Pounds')


class Temperature(RichConversionEnum):
    """Mapping of temperature unit conversions.

    IDs:
        1: Fahrenheit
        2: Celsius
        3: Kelvin
    """

    FAHRENHEIT_TO_CELSIUS = (1, 2, lambda x: (x - 32) * 5 / 9, 'Degree Celsius', 'Degrees Celsius')
    CELSIUS_TO_FAHRENHEIT = (
        2,
        1,
        lambda x: (x * 9 / 5) + 32,
        'Degree Fahrenheit',
        'Degrees Fahrenheit',
    )
    FAHRENHEIT_TO_KELVIN = (1, 3, lambda x: (x - 32) * 5 / 9 + 273.15, 'Kelvin', 'Kelvin')
    KELVIN_TO_FAHRENHEIT = (
        3,
        1,
        lambda x: (x - 273.15) * 9 / 5 + 32,
        'Degree Fahrenheit',
        'Degrees Fahrenheit',
    )
    CELSIUS_TO_KELVIN = (2, 3, lambda x: x + 273.15, 'Kelvin', 'Kelvin')
    KELVIN_TO_CELSIUS = (3, 2, lambda x: x - 273.15, 'Degree Celsius', 'Degrees Celsius')


class Pressure(RichConversionEnum):
    """Mapping of pressure unit conversions.

    IDs:
        1: Pascal
        2: Atmosphere
        3: Bar
    """

    PASCAL_TO_ATMOSPHERE = (1, 2, lambda x: x / 101325.0, 'Atmosphere', 'Atmospheres')
    ATMOSPHERE_TO_PASCAL = (2, 1, lambda x: x * 101325.0, 'Pascal', 'Pascals')
    PASCAL_TO_BAR = (1, 3, lambda x: x / 100000.0, 'Bar', 'Bars')
    BAR_TO_PASCAL = (3, 1, lambda x: x * 100000.0, 'Pascal', 'Pascals')
    ATMOSPHERE_TO_BAR = (2, 3, lambda x: x * 1.01325, 'Bar', 'Bars')
    BAR_TO_ATMOSPHERE = (3, 2, lambda x: x / 1.01325, 'Atmosphere', 'Atmospheres')
