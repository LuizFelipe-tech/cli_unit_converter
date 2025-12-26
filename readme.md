# 🔄 CLI Unit Converter

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-green?style=for-the-badge)](https://peps.python.org/pep-0008/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

A robust, interactive Command-Line Interface (CLI) tool aimed at converting various units of
measurement. Built with modern Python, emphasizing clean code, type safety, and user experience.

## 📖 Overview

This project provides a fast and reliable way to convert units across four major categories: **Length, Weight, Temperature, and Pressure**. It features a bidirectional conversion logic and an
intuitive text-based interface enhanced with ANSI color codes for better readability.

## ✨ Key Features

- **Multi-Category Support:**
    - 📏 **Length:** Meters ↔ Kilometers ↔ Miles
    - ⚖️ **Weight:** Kilograms ↔ Pounds ↔ Ounces
    - 🌡️ **Temperature:** Celsius ↔ Fahrenheit ↔ Kelvin
    - 🎈 **Pressure:** Pascal ↔ Atmosphere ↔ Bar
- **Robust Error Handling:** graceful management of invalid inputs prevents crashes and guides the
  user.
- **Modern Syntax:** Utilizes Python 3.10+ structural pattern matching (`match/case`) for clean
  control flow.
- **Type Safe:** Fully annotated with type hints for better maintainability and static analysis.

## 🛠️ Technical Highlights

*Designed with scalability and readability in mind.*

- **Modular Design:** Each conversion category is encapsulated in its own logical block.
- **Type Hinting:** Uses `from __future__ import annotations` and standard library typing to ensure
  code clarity and IDE support.
- **Input Validation:** A dedicated validation loop ensures that user input is sanitized before
  processing.
- **User Interface:** Uses ANSI escape codes for colored terminal output (Red for errors, Green for
  success/menus).

## 🚀 Getting Started

### Prerequisites

- **Python 3.10** or higher (required for `match/case` syntax).

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/cli-unit-converter.git](https://github.com/LuizFelipe-tech/cli_unit_converter)
   cd cli-unit-converter
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

## 📂 Project Structure

```text
cli-unit-converter/
├── src/
│   ├── main.py       # Entry point and core logic
│   └── exceptions.py # Custom exception classes
├── LICENSE           # MIT License
└── README.md         # Project documentation

