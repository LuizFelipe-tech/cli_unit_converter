# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
