# Text-to-Speech Clipboard Utility

A command-line utility that converts clipboard text to speech using various TTS engines.

## Features

- Reads text from clipboard and converts it to speech
- Supports multiple TTS engines:
  - Local models via Coqui TTS
  - Google Text-to-Speech (gTTS)
- Configurable via YAML file or command-line arguments
- Audio caching for improved performance
- Customizable voice parameters (speed, pitch, speaker)
- Cross-platform audio playback

## Installation

1. Create a Python virtual environment:
   ```bash
   python -m venv tts_py310_venv
   source tts_py310_venv/bin/activate  # On Windows: tts_py310_venv\Scripts\activate
   ```

2. Install required packages:
   ```bash
   pip install TTS gtts pyyaml pyperclip
   ```

3. Configure the YAML file (see Configuration section)

## Usage

Basic usage:

```

## Future Enhancements

See the [Future Requirements](#future-requirements) section below.

## Future Requirements

### High Priority
- [ ] Create keyboard shortcut to trigger the script
- [ ] Add voice selection menu with sample playback
- [ ] Implement sentence-by-sentence streaming for faster response
- [ ] Add support for reading selected text (not just clipboard)

### Medium Priority
- [ ] Create a simple GUI interface
- [ ] Add text preprocessing options (number expansion, abbreviation handling)
- [ ] Support for saving favorite voice configurations
- [ ] Background service mode that monitors clipboard changes

### Low Priority
- [ ] Integration with cloud TTS services (Azure, Amazon Polly)
- [ ] Voice emotion/style controls for supported models
- [ ] Audio post-processing options (normalization, compression)
- [ ] Export to podcast/audiobook formats with chapters

## Technical Debt & Improvements
- [ ] Refactor code into proper Python modules
- [ ] Add proper error handling and logging
- [ ] Create unit tests
- [ ] Add type hints for better code documentation
- [ ] Optimize model loading time