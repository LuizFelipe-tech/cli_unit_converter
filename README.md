# 🔄 CLI Unit Converter

[![Version](https://img.shields.io/badge/version-2.1.0-blue?style=for-the-badge)](https://github.com/seu-usuario/seu-repo](https://github.com/LuizFelipe-tech/cli_unit_converter/) [![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) [![CLI](https://img.shields.io/badge/CLI-Typer-009485?style=for-the-badge&logo=fastapi&logoColor=white)](https://typer.tiangolo.com/) [![UI](https://img.shields.io/badge/UI-Questionary-8E44AD?style=for-the-badge&logo=semantic-release&logoColor=white)](https://github.com/tmbo/questionary) [![Logging](https://img.shields.io/badge/Logging-Loguru-00AD00?style=for-the-badge&logo=python&logoColor=white)](https://github.com/Delgan/loguru) [![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

An **enterprise-grade**, highly modular Command-Line Interface (CLI) application for physical and digital unit conversions. Built with modern Python, it features both an intuitive interactive terminal UI and a robust **Natural Language Processing (NLP)** engine for zero-friction free-text conversions.

---

## 📖 Overview

Designed to handle extensive measurement systems, this project seamlessly bridges human readability and strict computational accuracy. Whether you prefer navigating through rich interactive menus using arrow keys or instantly parsing natural language arguments (e.g., *"100 GiB to bytes"*), the **CLI Unit Converter** adapts to your workflow.

---

## ✨ Key Features

### 🧠 Natural Language Parsing (NLP)

Type conversions as you think them. The custom regex-based NLP module instantly extracts numeric values, sources, and target units from free-text inputs.

### 🎮 Dual-Mode Interface

* **Interactive Mode:** Arrow-key navigation and elegant prompts powered by `Questionary`.
* **Headless Mode:** Single-command execution via `Typer` for pipeline/scripting integrations.

### 🌐 Expansive Multi-Domain Support

💾 Data Storage
* **Base:** Byte
* **Units:** Bit ↔ Byte ↔ Kibibyte (KiB) ↔ Mebibyte (MiB) ↔ Gibibyte (GiB) ↔ Tebibyte (TiB) ↔ Pebibyte (PiB)

📏 Length (Meters & Imperial)
* **Base:** Meter
* **Units:** Nanometer ↔ Millimeter ↔ Centimeter ↔ Meter ↔ Kilometer ↔ Inch ↔ Foot ↔ Yard ↔ Mile

⚖️ Weight & Mass
* **Base:** Kilogram
* **Units:** Milligram ↔ Gram ↔ Kilogram ↔ Metric Tonne ↔ Ounce ↔ Pound

🌡️ Temperature
* **Base:** Celsius
* **Units:** Celsius ↔ Fahrenheit ↔ Kelvin

🎈 Pressure
* **Base:** Pascal
* **Units:** Pascal ↔ Bar ↔ Atmosphere (atm) ↔ PSI ↔ Torr (mmHg)

🥛 Volume
* **Base:** Liter
* **Units:** Milliliter ↔ Liter ↔ Cubic Meter ($m^3$) ↔ US Fluid Ounce ↔ US Gallon

⏳ Time
* **Base:** Second
* **Units:** Nanosecond ↔ Microsecond ↔ Millisecond ↔ Second ↔ Minute ↔ Hour ↔ Day

⚡ Data Transfer Rate
* **Base:** Bits per second (bps)
* **Units:** bps ↔ Megabit/s (Mbps) ↔ Gigabit/s (Gbps) ↔ Megabyte/s (MB/s)

🔋 Energy
* **Base:** Joule
* **Units:** Joule ↔ Kilowatt-hour (kWh) ↔ Kilocalorie (kcal)

### 🛡️ Scientific Boundary Enforcement

Strictly validates physical limits, averting logic errors such as calculating temperatures below **Absolute Zero** or overflowing computational limits.

---

## 🛠️ Technical Highlights

Architected for maintainability, scalability, and a robust Developer Experience (DX).

* **Decoupled Architecture:** Strict separation of concerns divided into `core`, `config`, and `utils` modules, making the system highly testable and extensible.
* **Design Patterns:** Implements the **Registry Pattern** (`UnitConverter`) for dynamic unit discovery and $O(1)$ lookups, coupled with a **Base Unit Normalization** strategy that drastically reduces the permutations of conversion algorithms.
* **Advanced Telemetry:** Integrates `Loguru` for asynchronous, thread-safe, and structured logging. Debug traces are routed to isolated log files to preserve terminal cleanliness.
* **Strict Type Safety:** Fully annotated and verified using strict `Mypy` and `Pyright` configurations.
* **Robust Input Sanitization:** Utilizes unit name variations (e.g., mapping "mtr", "m", "meter" to a single registry key) to ensure high fault tolerance.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher.

### Installation

1. **Clone the repository:**

    ```bash
    git clone [https://github.com/LuizFelipe-tech/cli_unit_converter.git](https://github.com/LuizFelipe-tech/cli_unit_converter.git)
    cd cli-unit-converter
    ```

2. **Install dependencies:**

    ```bash
    pip install -e .
    # OR manually install the requirements
    pip install typer questionary loguru regex
    ```

### Usage

**Option 1: Free-Text NLP Mode (Fastest)**
Pass your conversion request directly as an argument:

```bash
python main.py "1024 kibibytes to bytes"
python main.py "100 km to miles"

```

**Option 2: Interactive CLI Mode**
Run the tool without arguments to enter the interactive menus:

```bash
python main.py

```

---

## 📂 Project Structure

```text
cli-unit-converter/
├── logs/                 # Telemetry and debug logs (git-ignored)
├── config/               # System Definitions
│   ├── enums.py          # Category enums and Registry Pattern implementation
│   ├── logging_config.py # Loguru sink & formatting configurations
│   └── unit_definition.py# Unit data structures
├── core/                 # Business Logic
│   ├── convert.py        # Conversion orchestration and validation rules
│   └── select_menu.py    # Questionary interactive UI logic
├── utils/                # Helper Modules
│   ├── nlp_module.py     # Regex-based natural language parser
│   └── validate_unit.py  # Cross-category validation
├── exceptions.py         # Domain-specific custom exceptions
├── main.py               # Typer application entry point
├── pyproject.toml        # Build system, Ruff, and Type-checking configs
└── README.md             # Project documentation

```

---

## 📜 Changelog

Please see `changelog.md` for a comprehensive history of feature additions, architectural shifts, and fixes.
