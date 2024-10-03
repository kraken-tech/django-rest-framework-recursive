# Changelog and Versioning

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2024-10-03

### Added

- Tested support for Python 3.12
- Tested support for Django versions 5.1

### Changed

### Removed

## [0.3.1] - 2024-09-03

### Added

### Changed

- Moved the dependencies for test packages (`pytest`, `pytest-django`, `pytest-cov`) into dev dependencies.

### Removed

## [0.3.0] - 2024-08-28

### Added

### Changed

- The package import semantics from `kraken.django_rest_framework_recursive` to `django_rest_framework_recursive`.
- Links in the README.md file to be to the correct files in the repository.
- The `pytest-django` version to be *minimum* `4.7.0` rather than *exactly* `4.7.0`.

### Removed

## [0.2.0] - 2024-08-22

### Added

- Tested support for Python 3.10 -> 3.11
- Tested support for Django versions 3.2 -> 5.0
- Tested support for Django REST Framework versions 3.12 -> 3.15
- Development support using MyPy, Ruff, and UV
- Pre-commit set-up to format before code is pushed

### Changed

- Formatting to follow Kraken open-source conventions
- Matrix testing runner from Tox to Nox

### Removed

- Tested support for all Python versions < 3.10.
- Tested support for all Django versions < 3.2
- Tested support for all Django REST Framework versions < 3.13.
- CI configuration on Travis
