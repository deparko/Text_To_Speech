#!/bin/bash
# Setup script for development environment
# This script sets up the development environment for the Text-to-Speech system

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "Setting up development environment in $SCRIPT_DIR"

# Copy combined requirements file from bin directory if it exists
BIN_DIR="$HOME/SoftwareDev/bin/tts"
if [ -f "$BIN_DIR/combined_requirements.txt" ]; then
    echo "Copying combined_requirements.txt from bin directory..."
    cp "$BIN_DIR/combined_requirements.txt" "$SCRIPT_DIR/"
else
    echo "Creating combined_requirements.txt..."
    cat > "$SCRIPT_DIR/combined_requirements.txt" << 'EOF'
# Combined requirements for TTS system with AI Text Processor integration
# =====================================================================

# Core TTS engines
gTTS>=2.5.0          # Google Text-to-Speech
openai>=1.65.0       # OpenAI TTS API (newer version takes precedence)

# Core utilities
pyperclip>=1.8.2     # Clipboard handling
PyYAML>=6.0.1        # Configuration file handling (newer version takes precedence)
pydub>=0.25.1        # Audio file manipulation
requests>=2.28.0     # HTTP requests for API calls

# File format support
python-docx>=1.0.0   # Word document support
PyPDF2>=3.0.0        # PDF file support

# Audio playback and handling
playsound>=1.3.0     # Cross-platform audio playback

# Optional utilities
Pillow>=11.0.0       # Image handling for podcast cover art

# Development tools (combined from both projects)
black>=24.0.0        # Code formatting (newer version takes precedence)
pylint>=3.0.0        # Code linting
pytest>=8.0.0        # Testing (newer version takes precedence)
isort>=5.12.0        # Import sorting
flake8>=6.0.0        # Code linting

# Optional dependencies for future expansion
# ollama client - uncomment when implementing Ollama support
# litellm>=0.13.0  # For unified API across providers

# System requirements:
# - Python 3.10 or higher
# - ffmpeg (for audio manipulation, install via system package manager)
#   macOS: brew install ffmpeg
#   Linux: apt-get install ffmpeg
#   Windows: download from https://ffmpeg.org/download.html
EOF
fi

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/.venv"
fi

# Activate virtual environment
source "$SCRIPT_DIR/.venv/bin/activate"
echo "Virtual environment activated"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from combined requirements file
echo "Installing dependencies from combined_requirements.txt..."
pip install -r "$SCRIPT_DIR/combined_requirements.txt"

# Check if AI Text Processor is available
AI_PROCESSOR_PATH="$HOME/SoftwareDev/AI-Text-Processor"
if [ -d "$AI_PROCESSOR_PATH" ]; then
    echo "AI Text Processor found at $AI_PROCESSOR_PATH"
    
    # Create symbolic link to AI Text Processor if it doesn't exist
    if [ ! -d "$SCRIPT_DIR/AI-Text-Processor" ]; then
        echo "Creating symbolic link to AI Text Processor..."
        ln -s "$AI_PROCESSOR_PATH" "$SCRIPT_DIR/AI-Text-Processor"
    fi
else
    echo "Warning: AI Text Processor not found at $AI_PROCESSOR_PATH"
    echo "AI-based filename generation may not work correctly"
fi

# Make speak script executable
chmod +x "$SCRIPT_DIR/speak"
echo "Made speak script executable"

# Create a development wrapper script
echo "Creating dev_speak script..."
cat > "$SCRIPT_DIR/dev_speak" << 'EOF'
#!/bin/bash
# Development wrapper script for text_to_speech.py
# Activates the virtual environment and runs the script with the provided arguments

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate the virtual environment
source "${SCRIPT_DIR}/.venv/bin/activate"

# Run the Python script with all arguments
python "${SCRIPT_DIR}/text_to_speech.py" "$@"

# Deactivate the virtual environment
deactivate
EOF
chmod +x "$SCRIPT_DIR/dev_speak"

# Print success message
echo ""
echo "Development environment setup complete!"
echo "You can now use the development version with:"
echo "cd $SCRIPT_DIR && ./dev_speak --list-ai-prompts"
echo ""
echo "To deploy changes to the bin directory, run:"
echo "./deploy_to_bin.sh"
echo ""

# Deactivate virtual environment
deactivate 