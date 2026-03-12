from __future__ import annotations

from config.enums import Category, UnitConverter, UnitDefinition

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
UnitConverter.register(
    'FOOT',
    UnitDefinition(
        'Foot',
        'Feet',
        Category.LENGTH,
        lambda x: x * 0.3048,  # foot -> meter
        lambda x: x / 0.3048,  # meter -> foot
    ),
)
UnitConverter.register(
    'INCH',
    UnitDefinition(
        'Inch',
        'Inches',
        Category.LENGTH,
        lambda x: x * 0.0254,  # inch -> meter
        lambda x: x / 0.0254,  # meter -> inch
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
# --- NOVA CATEGORIA: DATA_STORAGE (Base: Byte) ---
# Usando o padrão binário (IEC) que é o mais realista para alocação de memória e arquitetura de sistemas.
UnitConverter.register(
    'BYTE',
    UnitDefinition(
        'Byte',
        'Bytes',
        Category.DATA_STORAGE,
        lambda x: x,  # Already base unit.
        lambda x: x,
    ),
)
UnitConverter.register(
    'KIBIBYTE',
    UnitDefinition(
        'Kibibyte',
        'Kibibytes',
        Category.DATA_STORAGE,
        lambda x: x * 1024.0,  # KiB -> Byte
        lambda x: x / 1024.0,  # Byte -> KiB
    ),
)
UnitConverter.register(
    'MEBIBYTE',
    UnitDefinition(
        'Mebibyte',
        'Mebibytes',
        Category.DATA_STORAGE,
        lambda x: x * 1048576.0,  # MiB -> Byte (1024^2)
        lambda x: x / 1048576.0,  # Byte -> MiB
    ),
)
UnitConverter.register(
    'GIBIBYTE',
    UnitDefinition(
        'Gibibyte',
        'Gibibytes',
        Category.DATA_STORAGE,
        lambda x: x * 1073741824.0,  # GiB -> Byte (1024^3)
        lambda x: x / 1073741824.0,  # Byte -> GiB
    ),
)
