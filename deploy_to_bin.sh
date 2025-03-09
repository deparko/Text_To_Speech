#!/bin/bash
# Deployment script for the Text-to-Speech system
# This script copies the necessary files to the bin directory

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set the target directory
TARGET_DIR="$HOME/SoftwareDev/bin/tts"

echo "Deploying from $SCRIPT_DIR"
echo "Target directory: $TARGET_DIR"

# Check if the target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
fi

# Check if the tts_core directory exists in the target directory
if [ ! -d "$TARGET_DIR/tts_core" ]; then
    mkdir -p "$TARGET_DIR/tts_core"
fi

# Copy the main script
echo "Copying text_to_speech.py..."
cp "$SCRIPT_DIR/text_to_speech.py" "$TARGET_DIR/"

# Copy the speak script
echo "Copying speak script..."
cp "$SCRIPT_DIR/speak" "$TARGET_DIR/"

# Copy the add_to_path script
echo "Copying add_to_path.sh..."
cp "$SCRIPT_DIR/add_to_path.sh" "$TARGET_DIR/" 2>/dev/null || :
if [ -f "$TARGET_DIR/add_to_path.sh" ]; then
    chmod +x "$TARGET_DIR/add_to_path.sh"
fi

# Copy the tts_core files
echo "Copying tts_core files..."
cp "$SCRIPT_DIR/tts_core/ai_filename_generator.py" "$TARGET_DIR/tts_core/"
cp "$SCRIPT_DIR/tts_core/output_handler.py" "$TARGET_DIR/tts_core/"
cp "$SCRIPT_DIR/tts_core/openai_tts.py" "$TARGET_DIR/tts_core/"
cp "$SCRIPT_DIR/tts_core/gtts_engine.py" "$TARGET_DIR/tts_core/"

# Ensure __init__.py exists in the tts_core directory
if [ ! -f "$TARGET_DIR/tts_core/__init__.py" ]; then
    touch "$TARGET_DIR/tts_core/__init__.py"
fi

# Copy documentation
echo "Copying documentation..."
cp "$SCRIPT_DIR/README.md" "$TARGET_DIR/"
cp "$SCRIPT_DIR/AI_FILENAME_FEATURE.md" "$TARGET_DIR/" 2>/dev/null || :
cp "$SCRIPT_DIR/ENHANCEMENTS.md" "$TARGET_DIR/" 2>/dev/null || :
cp "$SCRIPT_DIR/KNOWN_ISSUES.md" "$TARGET_DIR/" 2>/dev/null || :
cp "$SCRIPT_DIR/SOFTWARE_PRINCIPLES.md" "$TARGET_DIR/" 2>/dev/null || :

# Copy tests directory
echo "Copying tests directory..."
if [ ! -d "$TARGET_DIR/tests" ]; then
    mkdir -p "$TARGET_DIR/tests"
fi
cp -r "$SCRIPT_DIR/tests/"* "$TARGET_DIR/tests/" 2>/dev/null || :
chmod +x "$TARGET_DIR/tests/"*.sh 2>/dev/null || :

# Check if combined_requirements.txt exists
if [ -f "$SCRIPT_DIR/combined_requirements.txt" ]; then
    echo "Copying combined_requirements.txt..."
    cp "$SCRIPT_DIR/combined_requirements.txt" "$TARGET_DIR/"
else
    echo "Creating combined_requirements.txt..."
    cat > "$TARGET_DIR/combined_requirements.txt" << 'EOL'
# Combined requirements for TTS system and AI Text Processor

# Core TTS engines
gTTS>=2.5.0
openai>=1.65.0

# Core utilities
pyperclip>=1.8.2
pyyaml>=6.0.1
python-dotenv>=1.0.0
requests>=2.31.0

# File format support
markdown>=3.5.1
pydub>=0.25.1

# Audio playback and handling
playsound>=1.3.0

# Optional utilities
tqdm>=4.66.1
colorama>=0.4.6

# Development tools
pytest>=8.0.0
black>=24.0.0
pylint>=3.0.3

# Optional dependencies for future expansion
# nltk>=3.8.1
# spacy>=3.7.2

# System requirements:
# - Python 3.10 or higher
# - ffmpeg for audio manipulation
EOL
fi

# Check if setup_integrated_env.sh exists
if [ ! -f "$TARGET_DIR/setup_integrated_env.sh" ]; then
    echo "Creating setup_integrated_env.sh..."
    cat > "$TARGET_DIR/setup_integrated_env.sh" << 'EOL'
#!/bin/bash
# Setup script for the integrated environment
# This script creates a virtual environment and installs all dependencies

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Setting up integrated environment in $SCRIPT_DIR"

# Check if the virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/.venv"
fi

# Activate the virtual environment
source "$SCRIPT_DIR/.venv/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r "$SCRIPT_DIR/combined_requirements.txt"

# Check if the AI Text Processor is available
AI_TEXT_PROCESSOR="$HOME/SoftwareDev/AI-Text-Processor"
if [ -d "$AI_TEXT_PROCESSOR" ]; then
    echo "Creating symbolic link to AI Text Processor..."
    ln -sf "$AI_TEXT_PROCESSOR" "$SCRIPT_DIR/AI-Text-Processor"
fi

# Make the speak script executable
chmod +x "$SCRIPT_DIR/speak"

# Print success message
echo "Setup complete!"
echo "You can now use the speak command to convert text to speech."
echo "Try: ./speak --list-ai-prompts"

# Deactivate the virtual environment
deactivate
EOL
    chmod +x "$TARGET_DIR/setup_integrated_env.sh"
fi

echo ""
echo "Deployment complete!"
echo "To set up the integrated environment, run:"
echo "cd $TARGET_DIR && ./setup_integrated_env.sh"
echo ""
echo "To add the TTS system to your PATH, run:"
echo "cd $TARGET_DIR && ./add_to_path.sh"
echo "" 