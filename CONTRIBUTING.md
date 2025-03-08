# Contributing to Text-To-Speech

Thank you for your interest in contributing to the Text-To-Speech project! This document provides guidelines and instructions for contributing.

## Development Setup

1. Clone the repository
2. Create a Python virtual environment (Python 3.10+ recommended)
3. Copy `tts_config.yaml.example` to `tts_config.yaml` and configure your settings
4. Install dependencies: `pip install -r requirements.txt`
5. Install development dependencies: `pip install black>=24.0.0 pylint>=3.0.0 pytest>=8.0.0`

## Development Process

1. Create a new branch for your feature/fix
2. Write tests for new functionality
3. Ensure all tests pass: `pytest`
4. Format code with Black: `black .`
5. Check code quality with Pylint: `pylint tts_core/`
6. Update documentation as needed
7. Update CHANGELOG.md following the Keep a Changelog format

## Pull Request Process

1. Ensure your code follows our style guidelines (Black + Pylint)
2. Update the README.md if needed
3. Add your changes to CHANGELOG.md under [Unreleased]
4. Submit a pull request with a clear description of changes
5. Wait for review and address any feedback

## Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting
- Maintain test coverage
- Write clear docstrings and comments
- Keep functions focused and modular

## Commit Messages

Follow the conventional commits format:
- feat: new feature
- fix: bug fix
- docs: documentation changes
- style: formatting
- refactor: code restructuring
- test: adding tests
- chore: maintenance

## Questions?

If you have questions, please open an issue for discussion. 