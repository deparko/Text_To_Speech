# Text-to-Speech Clipboard Utility

A command-line utility that converts text to speech using various TTS engines, with support for multiple input sources and iCloud Drive sync.

## Features

- Multiple input sources:
  - Clipboard text
  - Direct text input
  - File input (TXT, PDF, DOCX)
- Supports multiple TTS engines:
  - Local models via Coqui TTS (default: tacotron2-DDC)
  - Google Text-to-Speech (gTTS) as default
- Configurable via YAML file or command-line arguments
- Audio caching for improved performance (optional)
- Customizable voice parameters (speed, pitch, speaker)
- Cross-platform audio playback
- Clean, minimal console output with detailed logging
- macOS deployment support with keyboard shortcuts
- Text cleaning and preprocessing
- Modular architecture for easy maintenance and extension
- iCloud Drive integration:
  - Automatic sync across Apple devices
  - Organized file storage
  - Easy access via Files app

## Installation

1. Create a Python virtual environment:
   ```bash
   python3.10 -m venv .venv_tts310
   source .venv_tts310/bin/activate  # On Windows: .venv_tts310\Scripts\activate
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the YAML file (see Configuration section)

## Usage

Basic usage:
```bash
# Convert clipboard text to speech
speak

# Convert specific text to speech
speak --text "Your text here"

# Convert text from a file
speak --file "path/to/your/file.txt"

# Use Google TTS (default)
speak --text "Your text here"

# Use Coqui TTS instead
speak --text "Your text here" --use-coqui

# Adjust speech speed
speak --text "Your text here" --speed 1.2

# Save without playing
speak --text "Your text here" --no-play

# List available voices
speak --list-voices
```

## Configuration

The script can be configured via `tts_config.yaml`:

```yaml
model:
  name: "tts_models/en/ljspeech/tacotron2-DDC"  # Default TTS model
  alternatives:
    - "tts_models/en/ljspeech/fast_pitch"       # Faster model
    - "tts_models/en/vctk/fast_pitch"           # Multi-speaker fast model
    - "tts_models/en/vctk/vits"                 # Multi-speaker high quality
  use_gtts: true                                # Use Google TTS by default

gtts:
  language: "en"                                # Language code (e.g., en, fr, de, etc.)
  tld: "com"                                    # Top-level domain for the Google server
  slow: false                                   # Slower, more deliberate speech

voice:
  speed: 1.0                                    # Speech speed multiplier
  speaker_id: null                              # Speaker ID for multi-speaker models
  pitch: null                                   # Voice pitch adjustment
  sample_rate: 22050                            # Audio sample rate

output:
  folder: "~/Library/Mobile Documents/com~apple~CloudDocs/TTS_Audio"
  play_audio: true                              # Whether to play audio after generation
  cache_audio: false                            # Whether to cache generated audio

advanced:
  progress_bar: false                           # Show progress bar during generation
  gpu: false                                    # Use GPU for TTS processing
```

## Project Structure

```
Text_To_Speech/
├── tts_core/                   # Core functionality modules
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── input_handler.py       # Text input handling
│   ├── output_handler.py      # Audio output handling
│   └── utils.py              # Utility functions
├── text_to_speech.py         # Main script
├── tts_config.yaml           # Configuration file
└── requirements.txt          # Python dependencies
```

## macOS Deployment

1. Create the bin directory:
   ```bash
   mkdir -p ~/SoftwareDev/bin/tts
   ```

2. Copy the script and config:
   ```bash
   cp -r text_to_speech.py tts_core tts_config.yaml requirements.txt ~/SoftwareDev/bin/tts/
   ```

3. Set up virtual environment:
   ```bash
   cd ~/SoftwareDev/bin/tts
   python3.10 -m venv .venv_tts310
   source .venv_tts310/bin/activate
   pip install -r requirements.txt
   ```

4. Create wrapper script:
   ```bash
   echo '#!/bin/bash
   source ~/SoftwareDev/bin/tts/.venv_tts310/bin/activate
   cd ~/SoftwareDev/bin/tts
   python text_to_speech.py "$@"' > ~/SoftwareDev/bin/tts/speak
   chmod +x ~/SoftwareDev/bin/tts/speak
   ```

5. Add to PATH:
   ```bash
   echo 'export PATH="$HOME/SoftwareDev/bin/tts:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

## File Storage

Audio files are stored in iCloud Drive for easy access across devices:
- Location: `~/Library/Mobile Documents/com~apple~CloudDocs/TTS_Audio`
- Files are named with timestamps (e.g., `tts_20250306_213448.mp3`)
- Access via Files app on iOS/iPadOS devices
- Automatic sync across all Apple devices

## Future Development

For planned enhancements and improvements, see [ENHANCEMENTS.md](ENHANCEMENTS.md).