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
        ('meter', 'meters', 'm', 'metre', 'metres', 'mtr'),
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
        ('kilometer', 'kilometers', 'km', 'kilometre', 'kilometres', 'klick', 'klicks'),
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
        ('mile', 'miles', 'mi', 'mle'),
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
        ('foot', 'feet', 'ft', 'foots'),
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
        ('inch', 'inches', 'in', '"', "''"),
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
        ('kilogram', 'kilograms', 'kg', 'kgs', 'kilo', 'kilos'),
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
        ('pound', 'pounds', 'lb', 'lbs', '#'),
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
        ('ounce', 'ounces', 'oz', 'ozs'),
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
        ('celsius', 'degrees celsius', 'deg c', 'c', 'centigrade'),
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
        ('fahrenheit', 'degrees fahrenheit', 'deg f', 'f', 'farenheit'),
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
        ('kelvin', 'kelvins', 'k', 'degrees kelvin', 'deg k'),
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
        ('pascal', 'pascals', 'pa'),
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
        ('bar', 'bars'),
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
        ('atmosphere', 'atmospheres', 'atm', 'atms'),
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
        ('liter', 'liters', 'l', 'litre', 'litres', 'ltr'),
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
        ('milliliter', 'milliliters', 'ml', 'millilitre', 'millilitres', 'cc'),
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
        ('gallon', 'gallons', 'gal', 'us gal', 'us gallon'),
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
        ('byte', 'bytes', 'b'),
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
        ('kibibyte', 'kibibytes', 'kib', 'kb', 'kilobyte', 'kilobytes'),
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
        ('mebibyte', 'mebibytes', 'mib', 'mb', 'megabyte', 'megabytes'),
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
        ('gibibyte', 'gibibytes', 'gib', 'gb', 'gigabyte', 'gigabytes'),
    ),
)
