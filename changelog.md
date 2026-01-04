# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-04

### Added
- **Dependency:** Added [Rich](https://github.com/Textualize/rich) library for enhanced terminal UI and UX.
- **Architecture:** Implemented a **Registry Pattern** in `enums.py` via `UnitConverter` class to centralize logic.
- **Logic:** Adopted "Base Unit Normalization" strategy (e.g., converting everything to Meters first), reducing the number of required conversion formulas.
- **Validation:** Added generic `validate_physical_limits` to enforce scientific constraints (e.g., Absolute Zero checks for temperature, non-negative checks for scalar units).
- **Security:** Added checks for computational infinity (`math.isinf`) to prevent overflows.

### Changed
- **UI:** Replaced raw ANSI escape codes with `rich` Components (Panels, colored inputs) for a modern look.
- **Refactor:** Replaced repetitive handler functions in `main.py` with a single generic `handle_conversion` workflow.
- **Config:** Updated `pyproject.toml` to include `rich` as a required dependency.

### Removed
- Removed manual ANSI color constant definitions (`RED_TEXT`, `GREEN_TEXT`).
- Removed redundant conversion logic inside specific functions in favor of the unified `UnitConverter` methods.

## [1.0.0] - 2025-12-26

### Added

- Initial release of the CLI Unit Converter.
- **Conversion Modules:** Added support for Length, Weight, Temperature, and Pressure systems.
- **Interface:** implemented interactive CLI menu with ANSI color output (Red for errors, Green for
  success).
- **Architecture:** Created modular structure with `enums.py` for state management and
  `exceptions.py` for custom error handling.
- **Validation:** Implemented robust input validation loops to prevent crashes on invalid user
  input.
