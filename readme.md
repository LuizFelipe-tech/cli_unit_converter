# 🔄 CLI Unit Converter

![Version](https://img.shields.io/badge/version-1.1.1-blue?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Rich](https://img.shields.io/badge/UI-Rich-purple?style=for-the-badge)](https://github.com/Textualize/rich)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

A robust, interactive Command-Line Interface (CLI) tool aimed at converting various units of
measurement. Built with modern Python, emphasizing clean code, type safety, and user experience.

## 📖 Overview

This project provides a fast and reliable way to convert units across five major categories: *
*Length, Weight, Temperature, and more**. It features a bidirectional conversion logic and an
intuitive text-based interface enhanced with the rich library for better readability.

## ✨ Key Features

* **Multi-Category Support:**
    * 📏 **Length:** Meters ↔ Kilometers ↔ Miles
    * ⚖️ **Weight:** Kilograms ↔ Pounds ↔ Ounces
    * 🌡️ **Temperature:** Celsius ↔ Fahrenheit ↔ Kelvin
    * 🎈 **Pressure:** Pascal ↔ Atmosphere ↔ Bar
    * 🥛 **Volume:** Liters ↔ Milliliters ↔ US Gallons
* **Scientific Validation:** Enforces physical limits
  (e.g., prevents temperatures below Absolute Zero).
* **Modern UI:** Uses Rich Panels and colored feedback for a superior User Experience.
* **Type Safe:** Fully annotated with type hints for better maintainability and static analysis.

## 🛠️ Technical Highlights

*Designed with scalability and readability in mind.*

* **Observability:** Implements **Structured Logging** (via `structlog`) for silent, file-based
  debugging without polluting the CLI output.
* **Registry Pattern:** Uses a centralized `UnitConverter` class to manage unit definitions
  dynamically.
* **Enterprise Tooling:** Configured with `Ruff`, `Mypy` (Strict), and `Pyright` to ensure Pythonic
  best practices and type safety.
* **Normalization Strategy:** Converts all values to a "Base Unit" before converting to the target,
  reducing algorithmic complexity.

## 🚀 Getting Started

### Prerequisites

* **Python 3.10** or higher.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/cli-unit-converter.git](https://github.com/LuizFelipe-tech/cli_unit_converter)
   cd cli-unit-converter
   ```

2. **Install dependencies:**
    ```bash
    pip install -e .
    # OR manually install the requirement
    pip install rich
    pip install structlog
    ```


3. **Run the application:**
   ```bash
   python main.py
   ```

## 📂 Project Structure

```text
cli-unit-converter/
├── .github/
│   └── workflows/    # CI/CD Automation
├── logs/             # Git-ignored debug logs
├── src/
│   ├── main.py            # Entry point and core logic
│   ├── enums.py           # Domain Logic: Unit Registry & Conversion Engine
│   ├── exceptions.py      # Custom exception classes
│   └── logging_config.py  # Structured logging configuration
├── pyproject.toml    # Project metadata & Tooling config
└── README.md         # Project documentation
```

## 📜 Changelog

Please see [changelog.md](changelog.md) for more information on what has changed recently.
