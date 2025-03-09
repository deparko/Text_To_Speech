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
  - AI-powered text preprocessing for TTS optimization

- Enhanced playback features:
  - Interactive HTML player with progress tracking
  - Synchronized text highlighting
  - Click-to-seek functionality
  - Table of contents navigation

- AI Text Processor Integration:
  - Smart filename generation based on content
  - Text preprocessing for better TTS quality
  - Support for various AI prompts (simplify, cleanup_for_tts, etc.)
  - Seamless integration with OpenAI API

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Text_To_Speech
   ```

2. Set up the development environment:
   ```bash
   ./setup_dev_env.sh
   ```
   This script will:
   - Create a virtual environment
   - Install all dependencies
   - Set up symbolic links to the AI Text Processor
   - Create a development wrapper script

3. Install system dependencies:
   - For audio manipulation: `ffmpeg`
     ```bash
     # On macOS with Homebrew
     brew install ffmpeg
     
     # On Ubuntu/Debian
     sudo apt-get install ffmpeg
     
     # On Windows
     # Download from https://ffmpeg.org/download.html
     ```

4. Configure your API keys:
   - Copy `tts_config.yaml.example` to `tts_config.yaml`
   - Add your OpenAI API key if using OpenAI TTS

## Usage

### Basic Usage

1. From clipboard:
   ```bash
   ./dev_speak
   ```

2. From command line:
   ```bash
   ./dev_speak --text 'Text to convert to speech'
   ```
   **Note:** Use single quotes around text to avoid issues with shell interpretation.

3. From file:
   ```bash
   ./dev_speak --file input.txt
   ```

### Command Line Options

- `--text TEXT`: Text to convert to speech (use single quotes: `--text 'Your text here'`)
- `--file FILE`: Input file containing text
- `--voice VOICE`: OpenAI voice to use (nova, alloy, echo, fable, onyx, shimmer)
- `--use-gtts`: Use Google TTS instead of OpenAI
- `--speed SPEED`: Speech speed multiplier
- `--no-play`: Don't play audio after generation
- `--list-voices`: List available voices/models
- `--ai-prompt PROMPT`: Apply AI preprocessing with specified prompt
- `--list-ai-prompts`: List available AI prompts
- `--ai-filename`: Generate filename using AI based on content

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

## Development and Deployment

### Development Workflow

1. Make changes to the source code in the development environment
2. Test changes using the `dev_speak` script
3. Deploy changes to the bin directory:
   ```bash
   ./deploy_to_bin.sh
   ```
4. Set up the production environment (if not already set up):
   ```bash
   cd ~/SoftwareDev/bin/tts && ./setup_integrated_env.sh
   ```

### Available Scripts

- `setup_dev_env.sh`: Sets up the development environment
- `dev_speak`: Runs the TTS script in the development environment
- `deploy_to_bin.sh`: Deploys changes to the bin directory
- `setup_integrated_env.sh`: Sets up the production environment in the bin directory

### AI Text Processor Integration

The TTS system integrates with the AI Text Processor to provide:

1. **AI-powered text preprocessing**: Optimize text for TTS using various prompts:
   - `--ai-cleanup_for_tts`: Converts numbers, abbreviations, and symbols to their spoken form
   - `--ai-simplify`: Makes complex text easier to understand
   - `--ai-expand`: Expands abbreviations and acronyms
   - And more (use `--list-ai-prompts` to see all available prompts)

2. **Smart filename generation**: Generate descriptive filenames based on content:
   ```bash
   ./dev_speak --text "The mitochondria is the powerhouse of the cell" --ai-summarize
   ```
   This might generate a file named "Cellular_Energy_Production.mp3" instead of a timestamp-based name.

> **Note**: Some complex texts may cause issues with OpenAI TTS when using AI prompts. If you encounter errors, try using Google TTS instead by adding the `--use-gtts` flag.

For more information on the AI filename generation feature, see [AI_FILENAME_FEATURE.md](AI_FILENAME_FEATURE.md).

## Testing

### Manual Testing

1. **Basic TTS Functionality**:
   ```bash
   ./dev_speak --text "This is a test of the text-to-speech system."
   ```
   Verify that the audio is generated and played correctly.

2. **AI Text Preprocessing**:
   ```bash
   ./dev_speak --text "On 4/15/2023, Dr. Smith met with 3 patients at 123 Main St." --ai-cleanup_for_tts
   ```
   Verify that the text is properly converted to "On April fifteenth, twenty twenty-three, Doctor Smith met with three patients at one two three Main Street."

3. **AI Filename Generation**:
   ```bash
   ./dev_speak --text "The mitochondria is the powerhouse of the cell" --ai-summarize
   ```
   Verify that a descriptive filename is generated instead of a timestamp-based one.

4. **List Available AI Prompts**:
   ```bash
   ./dev_speak --list-ai-prompts
   ```
   Verify that a list of available AI prompts is displayed.

5. **Different TTS Engines**:
   ```bash
   ./dev_speak --text "Testing Google TTS" --use-gtts
   ```
   Verify that the Google TTS engine is used instead of OpenAI.

6. **Different Voices**:
   ```bash
   ./dev_speak --text "Testing different voices" --voice alloy
   ```
   Verify that the specified voice is used.

7. **File Input**:
   ```bash
   echo "This is a test from a file" > test_input.txt
   ./dev_speak --file test_input.txt
   ```
   Verify that the text from the file is processed correctly.

8. **Clipboard Input**:
   Copy some text to the clipboard, then run:
   ```bash
   ./dev_speak
   ```
   Verify that the text from the clipboard is processed correctly.

### Automated Testing

The project includes a test suite that can be run using pytest:

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run all tests
pytest

# Run specific test categories
pytest tests/test_tts_engines.py
pytest tests/test_ai_integration.py

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=tts_core
```

#### Test Categories

1. **Unit Tests**: Test individual components in isolation
   - TTS engines
   - Input/output handlers
   - Configuration management
   - AI integration

2. **Integration Tests**: Test how components work together
   - End-to-end text processing
   - File generation
   - AI preprocessing

3. **Regression Tests**: Ensure that fixed bugs don't reappear

#### Writing New Tests

When adding new features or fixing bugs, always add corresponding tests:

1. Create a new test file in the `tests` directory if needed
2. Follow the existing test structure
3. Use pytest fixtures for common setup
4. Mock external dependencies (APIs, file system, etc.)

Example test for AI filename generation:

```python
def test_ai_filename_generation():
    from tts_core.ai_filename_generator import generate_ai_filename
    
    # Test with sample text
    text = "The mitochondria is the powerhouse of the cell"
    filename = generate_ai_filename(text)
    
    # Verify that the filename is not empty and doesn't contain invalid characters
    assert filename
    assert '/' not in filename
    assert '\\' not in filename
    
    # Verify that the filename is somewhat descriptive of the content
    assert any(word in filename.lower() for word in ['cell', 'mitochondria', 'power'])
```

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

### Running from Any Directory

To run the `speak` command from any directory:

1. Add the TTS system to your PATH:
   ```bash
   cd ~/SoftwareDev/bin/tts && ./add_to_path.sh
   ```

2. Restart your shell or run:
   ```bash
   source ~/.zshrc  # or ~/.bashrc for bash users
   ```

3. Now you can use the speak command from any directory:
   ```bash
   speak --text 'Hello, world!'
   ```
   **Note:** Always use single quotes around text to avoid issues with shell interpretation.