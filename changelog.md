# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-03-26

### 🚀 Added

* **New Measurement Categories:** Expanded the `Category` enum and unit registry to support **Time**, **Data Transfer Rate**, and **Energy**.
* **Expanded Unit Registry:** * *Time:* Ranging from nanoseconds to days (base: seconds).
  * *Data Transfer Rate:* SI decimal bits (Mbps, Gbps) and bytes (MB/s).
  * *Energy:* Joules, Kilowatt-hours, and Kilocalories.
  * *Data Storage:* Introduced higher-capacity units (Tebibyte, Pebibyte) and the fundamental Bit.
  * *Existing Categories:* Added centimeters, metric tonnes, PSI, and cubic meters to Length, Weight, Pressure, and Volume.
* **Parsing Robustness:** Introduced multiple string aliases (e.g., `"mmhg"` for Torr, `"klick"` for Kilometers) to improve input flexibility and NLP accuracy.
* **Documentation:** Added comprehensive module-level docstrings to `unit_definition.py` and `validate_unit.py` to clarify responsibilities.

### 🔄 Changed

* **Codebase Internationalization:** Standardized internal variable names (`chave` -> `key`, etc.), log messages, and comments from Portuguese to English for global maintainability.
* **Code Quality & Type Safety:** Added explicit type hints to configuration functions (e.g., `validate_unit_categories`) and corrected inaccurate docstrings across the project.
* **Error Handling:** Improved resilience in the main entry point (`main.py`) by replacing a bare `except:` block with a targeted `except Exception:` catch.
* **Execution:** Added the `#!/usr/bin/env python3` shebang to `main.py` to support direct script execution.

## [2.0.0] - 2026-03-15

### 🚀 Added

* **Natural Language Processing (NLP):** Introduced free-text parsing capabilities. Users can now pass direct natural language arguments to the CLI (e.g., `"100 km to miles"`), which are automatically parsed and converted via the new `nlp_module`.
* **New Domain (Data Storage):** Added support for digital storage capacity conversions using the realistic binary standard (IEC). Supported units include Byte, Kibibyte, Mebibyte, and Gibibyte.
* **Interactive CLI UI:** Integrated `Questionary` to provide a modern, interactive terminal experience. Users now navigate categories and units using arrow keys instead of typing menu numbers.
* **CLI Framework:** Adopted `Typer` as the foundational framework to robustly handle command-line arguments, options, and application entry points.
* **Unit Name Variations:** Expanded the `UnitDefinition` data structure to include `name_variations` (e.g., mapping `"m"`, `"meter"`, and `"mtr"` to `METER`) to ensure accurate cross-matching during NLP requests.

### 🔄 Changed

* **Major Architecture Restructuring:** Completely reorganized the codebase into a modular package layout (`core/`, `config/`, `utils/`) to adhere to strict separation of concerns and improve maintainability.
* **Logging Engine:** Migrated the core application logging framework from `structlog` to `Loguru` for more expressive and streamlined debug tracing.
* **Conversion Workflow:** Overhauled the `handle_conversion` orchestration to seamlessly support both interactive (`Questionary`) flows and direct CLI argument (`Typer`) execution.

### 🗑️ Removed

* **Legacy UI System:** Completely removed the `Rich` library dependency and the old numeric console panel menus (e.g., `get_valid_number`, `get_menu_option`) in favor of the new interactive selection prompts.

## [1.2.1] - 2026-01-23

### Fixed

* **Logging:** Fixed an issue where debug logs were appearing in the CLI output. Logs are now correctly restricted to `converter_debug.log`.

## [1.2.0] - 2026-01-23

### Added

* **New Domain:** Added **Volume** category support with conversions for Liters, Milliliters, and US Gallons.
* **Observability:** Implemented **Structured Logging** (`structlog`) to capture debug data silently to `logs/converter_debug.log`, keeping the UI clean.
* **CI/CD:** Added `.github/workflows/release.yml` to automate GitHub Releases upon tagging versions (e.g., `v1.2.0`).
* **Development Experience:** Added enterprise-grade configuration for `Ruff` (linter/formatter), `Mypy` (strict typing), and `Bumpver` in `pyproject.toml`.

### Changed

* **Architecture:** Decoupled logging configuration into `src/logging_config.py` to adhere to Single Responsibility Principle.
* **Dependencies:** Updated `pyproject.toml` to include `structlog` and explicit build-system requirements.

## [1.1.1] - 2026-01-04

### Added

* **Dynamic Registry:** Added get_keys_by_category to UnitConverter to allow dynamic discovery of units.

* **Category Metadata:** Added display_name and min_value_base properties to the Category enum to centralize domain rules and UI strings.

### Changed

* **UI Orchestration:** Refactored main.py to generate the main menu and unit sub-menus dynamically by iterating over categories and the unit registry.

* **Validation Engine:** Unified physical limit checks in validate_physical_limits using the new min_value_base property, ensuring consistent validation across all measurement types.

* **Refined Data Structures:** Removed redundant id and category_name from UnitDefinition to follow DRY (Don't Repeat Yourself) principles.

### Fixed

* **Accuracy:** Improved physical limit validation by performing comparisons in the base unit (e.g., Kelvin/Celsius normalization) before triggering warnings.

## [1.1.0] - 2026-01-04

### Added

* **Dependency:** Added [Rich](https://github.com/Textualize/rich) library for enhanced terminal UI and UX.
* **Architecture:** Implemented a **Registry Pattern** in `enums.py` via `UnitConverter` class to centralize logic.
* **Logic:** Adopted "Base Unit Normalization" strategy (e.g., converting everything to Meters first), reducing the number of required conversion formulas.
* **Validation:** Added generic `validate_physical_limits` to enforce scientific constraints (e.g., Absolute Zero checks for temperature, non-negative checks for scalar units).
* **Security:** Added checks for computational infinity (`math.isinf`) to prevent overflows.

### Changed

* **UI:** Replaced raw ANSI escape codes with `rich` Components (Panels, colored inputs) for a modern look.
* **Refactor:** Replaced repetitive handler functions in `main.py` with a single generic `handle_conversion` workflow.
* **Config:** Updated `pyproject.toml` to include `rich` as a required dependency.

### Removed

* Removed manual ANSI color constant definitions (`RED_TEXT`, `GREEN_TEXT`).
* Removed redundant conversion logic inside specific functions in favor of the unified `UnitConverter` methods.

## [1.0.0] - 2025-12-26

### Added

* Initial release of the CLI Unit Converter.
* **Conversion Modules:** Added support for Length, Weight, Temperature, and Pressure systems.
* **Interface:** implemented interactive CLI menu with ANSI color output (Red for errors, Green for
  success).
* **Architecture:** Created modular structure with `enums.py` for state management and
  `exceptions.py` for custom error handling.
* **Validation:** Implemented robust input validation loops to prevent crashes on invalid user
  input.
