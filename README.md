# Text-to-Speech Utility

A powerful text-to-speech conversion utility that supports multiple TTS engines and provides rich output formats.

## Features

- Multiple TTS engine support:
  - OpenAI TTS (default)
  - Google Text-to-Speech (gTTS)
  - More engines planned

- Rich output formats:
  - MP3 audio files
  - Interactive HTML viewer with synchronized text
  - Markdown files with metadata and timestamps
  - SRT subtitle files for video integration

- Advanced text processing:
  - Smart text segmentation
  - Quote detection and formatting
  - Automatic timing calculation
  - Support for various input formats (clipboard, file, command line)

- Enhanced playback features:
  - Interactive HTML player with progress tracking
  - Synchronized text highlighting
  - Click-to-seek functionality
  - Table of contents navigation

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Text_To_Speech
   ```

2. Create and activate a Python virtual environment (Python 3.10+ required):
   ```bash
   python -m venv .venv_tts310
   source .venv_tts310/bin/activate  # On Unix/macOS
   # or
   .venv_tts310\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install system dependencies:
   - For audio manipulation: `ffmpeg`
     ```bash
     # On macOS with Homebrew
     brew install ffmpeg
     
     # On Ubuntu/Debian
     sudo apt-get install ffmpeg
     
     # On Windows
     # Download from https://ffmpeg.org/download.html
     ```

5. Configure your API keys:
   - Copy `tts_config.yaml.example` to `tts_config.yaml`
   - Add your OpenAI API key if using OpenAI TTS

## Usage

### Basic Usage

1. From clipboard:
   ```bash
   ./speak
   ```

2. From command line:
   ```bash
   ./speak --text "Text to convert to speech"
   ```

3. From file:
   ```bash
   ./speak --file input.txt
   ```

### Command Line Options

- `--text TEXT`: Text to convert to speech
- `--file FILE`: Input file containing text
- `--voice VOICE`: OpenAI voice to use (nova, alloy, echo, fable, onyx, shimmer)
- `--use-gtts`: Use Google TTS instead of OpenAI
- `--speed SPEED`: Speech speed multiplier
- `--no-play`: Don't play audio after generation
- `--list-voices`: List available voices/models

### Output Files

For each conversion, the following files are generated in your configured output directory:

1. Audio File (`tts_YYYYMMDD_HHMMSS.mp3`):
   - High-quality audio output
   - Compatible with most media players

2. HTML Viewer (`tts_YYYYMMDD_HHMMSS.html`):
   - Interactive audio player
   - Synchronized text display
   - Navigation features
   - Metadata display

3. Markdown File (`tts_YYYYMMDD_HHMMSS.md`):
   - Text content with metadata
   - Table of contents
   - Timestamps
   - Formatted quotes

4. SRT Subtitle File (`tts_YYYYMMDD_HHMMSS.srt`):
   - Standard subtitle format
   - Compatible with video players
   - Timing information

### HTML Viewer Features

The HTML viewer provides an enhanced playback experience:

- Sticky audio player that stays visible while scrolling
- Progress bar showing current position
- Table of contents with clickable timestamps
- Auto-scrolling to current segment
- Quote highlighting
- Metadata display (duration, word count, etc.)
- Click-to-seek functionality

## Configuration

The `tts_config.yaml` file allows you to configure:

- API keys and engine selection
- Output directory and format
- Audio caching settings
- Playback preferences
- Voice and speed settings

## Development

- Python 3.10 or higher required
- Uses `black` for code formatting
- Uses `pylint` for code quality
- Uses `pytest` for testing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## License

[Your license information here]

## Acknowledgments

- OpenAI for their TTS API
- Google for gTTS
- All contributors and users

For more information, see:
- [ENHANCEMENTS.md](ENHANCEMENTS.md) for planned features
- [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for current limitations
- [SOFTWARE_PRINCIPLES.md](SOFTWARE_PRINCIPLES.md) for development guidelines