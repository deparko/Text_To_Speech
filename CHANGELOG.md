# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Security
- Removed sensitive configuration data from repository
- Added template configuration file
- Updated gitignore rules for sensitive files

### Changed
- Updated configuration structure and dependencies
- Enhanced documentation with new features and known issues
- Improved core functionality with better text processing
- Enhanced output generation capabilities

### Added
- New TTS engines support
- HTML viewer for synchronized text/audio playback
- Initial test suite
- Comprehensive documentation (README, KNOWN_ISSUES, ENHANCEMENTS)
- AI-generated filenames feature that creates descriptive filenames based on text content
- Integration with AI Text Processor for intelligent text analysis
- Command-line arguments for controlling AI filename generation:
  - `--no-ai-filename`: Disable AI-generated filenames
  - `--list-ai-prompts`: List available AI prompts
  - `--ai-<prompt>`: Use a specific prompt for filename generation
- Documentation for the AI filename feature in AI_FILENAME_FEATURE.md

## [1.0.0] - 2025-03-06

### Changed
- Simplified storage to iCloud Drive
- Deprecated Apple Music integration
- Updated documentation structure

### Added
- Initial release of Text-to-Speech utility
- Basic text processing functionality
- OpenAI TTS integration
- Command-line interface
- Configuration system
- Logging system
- Error handling
- Audio file management
- Initial release of the Text-to-Speech system
- Support for OpenAI TTS and Google TTS engines
- Command-line interface with various options
- Clipboard integration for easy text input
- Automatic generation of SRT, markdown, and HTML files
- Audio caching for improved performance

[Unreleased]: https://github.com/yourusername/Text-To-Speech/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/Text-To-Speech/releases/tag/v1.0.0 