"""Unit definitions and registration.

Registers all supported units with their respective metadata, conversion
formulas (to/from base units), and common variations/aliases.
"""

from __future__ import annotations

from config.enums import Category, UnitConverter, UnitDefinition

# --- Unit Registration ---

# --- LENGTH (Base: Meters)
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
    'CENTIMETER',
    UnitDefinition(
        'Centimeter',
        'Centimeters',
        Category.LENGTH,
        lambda x: x / 100.0,  # centimeter -> meter
        lambda x: x * 100.0,  # meter -> centimeter
        ('centimeter', 'centimeters', 'cm'),
    ),
)
UnitConverter.register(
    'MILLIMETER',
    UnitDefinition(
        'Millimeter',
        'Millimeters',
        Category.LENGTH,
        lambda x: x / 1000.0,  # millimeter -> meter
        lambda x: x * 1000.0,  # meter -> millimeter
        ('millimeter', 'millimeters', 'mm'),
    ),
)
UnitConverter.register(
    'NANOMETER',
    UnitDefinition(
        'Nanometer',
        'Nanometers',
        Category.LENGTH,
        lambda x: x / 1e9,  # nanometer -> meter
        lambda x: x * 1e9,  # meter -> nanometer
        ('nanometer', 'nanometers', 'nm'),
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
    'YARD',
    UnitDefinition(
        'Yard',
        'Yards',
        Category.LENGTH,
        lambda x: x * 0.9144,  # yard -> meter
        lambda x: x / 0.9144,  # meter -> yard
        ('yard', 'yards', 'yd'),
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

# --- WEIGHT (Base: Kilograms)
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
    'TONNE',
    UnitDefinition(
        'Metric Tonne',
        'Metric Tonnes',
        Category.WEIGHT,
        lambda x: x * 1000.0,  # tonne -> kilogram
        lambda x: x / 1000.0,  # kilogram -> tonne
        ('tonne', 'tonnes', 't', 'metric ton'),
    ),
)
UnitConverter.register(
    'GRAM',
    UnitDefinition(
        'Gram',
        'Grams',
        Category.WEIGHT,
        lambda x: x / 1000.0,  # gram -> kilogram
        lambda x: x * 1000.0,  # kilogram -> gram
        ('gram', 'grams', 'g'),
    ),
)
UnitConverter.register(
    'MILLIGRAM',
    UnitDefinition(
        'Milligram',
        'Milligrams',
        Category.WEIGHT,
        lambda x: x / 1e6,  # milligram -> kilogram
        lambda x: x * 1e6,  # kilogram -> milligram
        ('milligram', 'milligrams', 'mg'),
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

# --- TEMPERATURE (Base: Celsius)
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

# --- PRESSURE (Base: Pascal)
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
UnitConverter.register(
    'PSI',
    UnitDefinition(
        'Pound per square inch',
        'Pounds per square inch',
        Category.PRESSURE,
        lambda x: x * 6894.76,  # psi -> Pascal
        lambda x: x / 6894.76,  # Pascal -> psi
        ('psi', 'pound per square inch', 'lbf/in2'),
    ),
)
UnitConverter.register(
    'TORR',
    UnitDefinition(
        'Torr',
        'Torr',
        Category.PRESSURE,
        lambda x: x * 133.322,  # torr (mmHg) -> Pascal
        lambda x: x / 133.322,  # Pascal -> torr
        ('torr', 'mmhg', 'millimeters of mercury'),
    ),
)

# --- VOLUME (Base: Liters)
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
    'CUBIC_METER',
    UnitDefinition(
        'Cubic Meter',
        'Cubic Meters',
        Category.VOLUME,
        lambda x: x * 1000.0,  # m3 -> liter
        lambda x: x / 1000.0,  # liter -> m3
        ('cubic meter', 'cubic meters', 'm3', 'm^3'),
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
UnitConverter.register(
    'FLUID_OUNCE_US',
    UnitDefinition(
        'US Fluid Ounce',
        'US Fluid Ounces',
        Category.VOLUME,
        lambda x: x * 0.0295735,  # fl oz -> liter
        lambda x: x / 0.0295735,  # liter -> fl oz
        ('fluid ounce', 'fluid ounces', 'fl oz', 'oz fl'),
    ),
)

# --- DATA_STORAGE (Base: Byte)
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
UnitConverter.register(
    'TEBIBYTE',
    UnitDefinition(
        'Tebibyte',
        'Tebibytes',
        Category.DATA_STORAGE,
        lambda x: x * 1099511627776.0,  # TiB -> Byte (1024^4)
        lambda x: x / 1099511627776.0,  # Byte -> TiB
        ('tebibyte', 'tebibytes', 'tib', 'tb', 'terabyte', 'terabytes'),
    ),
)
UnitConverter.register(
    'PEBIBYTE',
    UnitDefinition(
        'Pebibyte',
        'Pebibytes',
        Category.DATA_STORAGE,
        lambda x: x * 1125899906842624.0,  # PiB -> Byte (1024^5)
        lambda x: x / 1125899906842624.0,  # Byte -> PiB
        ('pebibyte', 'pebibytes', 'pib', 'pb', 'petabyte', 'petabytes'),
    ),
)
UnitConverter.register(
    'BIT',
    UnitDefinition(
        'Bit',
        'Bits',
        Category.DATA_STORAGE,
        lambda x: x / 8.0,  # bit -> byte
        lambda x: x * 8.0,  # byte -> bit
        ('bit', 'bits', 'b'),
    ),
)

# --- TIME (Base: Seconds)
UnitConverter.register(
    'SECOND',
    UnitDefinition(
        'Second',
        'Seconds',
        Category.TIME,
        lambda x: x,  # Already base unit.
        lambda x: x,
        ('second', 'seconds', 's', 'sec', 'secs'),
    ),
)
UnitConverter.register(
    'MILLISECOND',
    UnitDefinition(
        'Millisecond',
        'Milliseconds',
        Category.TIME,
        lambda x: x / 1000.0,
        lambda x: x * 1000.0,
        ('millisecond', 'milliseconds', 'ms'),
    ),
)
UnitConverter.register(
    'MICROSECOND',
    UnitDefinition(
        'Microsecond',
        'Microseconds',
        Category.TIME,
        lambda x: x / 1e6,  # microsecond -> second
        lambda x: x * 1e6,  # second -> microsecond
        ('microsecond', 'microseconds', 'us', 'µs'),
    ),
)
UnitConverter.register(
    'NANOSECOND',
    UnitDefinition(
        'Nanosecond',
        'Nanoseconds',
        Category.TIME,
        lambda x: x / 1e9,
        lambda x: x * 1e9,
        ('nanosecond', 'nanoseconds', 'ns'),
    ),
)
UnitConverter.register(
    'MINUTE',
    UnitDefinition(
        'Minute',
        'Minutes',
        Category.TIME,
        lambda x: x * 60.0,
        lambda x: x / 60.0,
        ('minute', 'minutes', 'min', 'mins'),
    ),
)
UnitConverter.register(
    'HOUR',
    UnitDefinition(
        'Hour',
        'Hours',
        Category.TIME,
        lambda x: x * 3600.0,
        lambda x: x / 3600.0,
        ('hour', 'hours', 'h', 'hr', 'hrs'),
    ),
)
UnitConverter.register(
    'DAY',
    UnitDefinition(
        'Day',
        'Days',
        Category.TIME,
        lambda x: x * 86400.0,
        lambda x: x / 86400.0,
        ('day', 'days', 'd'),
    ),
)

# --- DATA_TRANSFER_RATE (Base: Bits per second)
UnitConverter.register(
    'BPS',
    UnitDefinition(
        'Bit per second',
        'Bits per second',
        Category.DATA_TRANSFER_RATE,
        lambda x: x,  # Already base unit.
        lambda x: x,
        ('bps', 'bit/s', 'bits/s'),
    ),
)
UnitConverter.register(
    'MBPS',
    UnitDefinition(
        'Megabit per second',
        'Megabits per second',
        Category.DATA_TRANSFER_RATE,
        lambda x: x * 1000000.0,  # Assuming SI standard for networks (base 10)
        lambda x: x / 1000000.0,
        ('mbps', 'mbit/s', 'megabit/s'),
    ),
)
UnitConverter.register(
    'GBPS',
    UnitDefinition(
        'Gigabit per second',
        'Gigabits per second',
        Category.DATA_TRANSFER_RATE,
        lambda x: x * 1e9,  # Gbps -> bps
        lambda x: x / 1e9,  # bps -> Gbps
        ('gbps', 'gbit/s', 'gigabit/s'),
    ),
)
UnitConverter.register(
    'MB_PER_SEC',
    UnitDefinition(
        'Megabyte per second',
        'Megabytes per second',
        Category.DATA_TRANSFER_RATE,
        lambda x: x * 8000000.0,  # MB/s -> bps (1 Byte = 8 bits, decimal base for network)
        lambda x: x / 8000000.0,  # bps -> MB/s
        ('mb/s', 'mbyte/s', 'megabytes per second'),  # Vital distinction: MB/s vs Mbps
    ),
)

# --- ENERGY (Base: Joule)
UnitConverter.register(
    'JOULE',
    UnitDefinition(
        'Joule',
        'Joules',
        Category.ENERGY,
        lambda x: x,  # Already base unit.
        lambda x: x,
        ('joule', 'joules', 'j'),
    ),
)
UnitConverter.register(
    'KILOWATT_HOUR',
    UnitDefinition(
        'Kilowatt-hour',
        'Kilowatt-hours',
        Category.ENERGY,
        lambda x: x * 3600000.0,  # kWh -> Joules
        lambda x: x / 3600000.0,  # Joules -> kWh
        ('kwh', 'kilowatt-hour', 'kilowatt-hours'),
    ),
)
UnitConverter.register(
    'KILOCALORIE',
    UnitDefinition(
        'Kilocalorie',
        'Kilocalories',
        Category.ENERGY,
        lambda x: x * 4184.0,  # kcal -> Joules
        lambda x: x / 4184.0,  # Joules -> kcal
        ('kcal', 'kilocalorie', 'kilocalories', 'calorie', 'calories'),
    ),
)
