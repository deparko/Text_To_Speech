#!/bin/bash
# Test the deployment setup with the "speak" command

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print section header
print_header() {
    echo -e "\n${YELLOW}=======================================${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${YELLOW}=======================================${NC}"
}

# Function to print step
print_step() {
    echo -e "\n${BLUE}$1${NC}"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Create deployment directory
setup_deployment() {
    print_step "Setting up deployment directory..."
    
    # Create deployment directory
    mkdir -p ~/SoftwareDev/bin/tts/tts_core
    
    # Copy files
    print_step "Copying files to deployment directory..."
    cp "$(dirname "$0")/../text_to_speech.py" ~/SoftwareDev/bin/tts/
    cp "$(dirname "$0")/../requirements.txt" ~/SoftwareDev/bin/tts/
    
    # Copy tts_core files
    cp "$(dirname "$0")/../tts_core/"*.py ~/SoftwareDev/bin/tts/tts_core/
    
    # Create config file if it doesn't exist
    if [ ! -f ~/SoftwareDev/bin/tts/tts_config.yaml ]; then
        print_step "Creating config file..."
        cat > ~/SoftwareDev/bin/tts/tts_config.yaml << EOF
# TTS Configuration File

# Model Settings
model:
  name: "tts_models/en/ljspeech/tacotron2-DDC"
  use_gtts: true  # Use Google TTS for testing

# Voice Settings
voice:
  speed: 1.0
  speaker_id: null
  pitch: null

# Output Settings
output:
  folder: "~/Documents/TTS_Audio"
  play_audio: false
  cache_audio: true
  output_only: true
EOF
    fi
    
    # Create speak script
    print_step "Creating speak script..."
    cat > ~/SoftwareDev/bin/tts/speak << EOF
#!/bin/bash

# Activate virtual environment if it exists
if [ -d "\$(dirname "\$0")/.venv" ]; then
    source "\$(dirname "\$0")/.venv/bin/activate"
fi

# Change to the script directory
cd "\$(dirname "\$0")"

# Run the script with all arguments passed to this command
python text_to_speech.py "\$@"

# Deactivate virtual environment if it was activated
if [ -n "\$VIRTUAL_ENV" ]; then
    deactivate
fi
EOF
    
    # Make speak script executable
    chmod +x ~/SoftwareDev/bin/tts/speak
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ~/SoftwareDev/bin/tts/.venv ]; then
        print_step "Creating virtual environment..."
        cd ~/SoftwareDev/bin/tts
        python -m venv .venv
        source .venv/bin/activate
        
        # Install only the essential dependencies for testing
        print_step "Installing essential dependencies..."
        pip install PyYAML pyperclip gtts
        
        deactivate
    fi
    
    print_step "Deployment setup complete!"
}

# Test the speak command with manual dependency check
test_speak_command() {
    print_header "Testing 'speak' command"
    
    # Check if speak command exists
    if [ -f ~/SoftwareDev/bin/tts/speak ]; then
        print_step "Checking dependencies..."
        
        # Activate the virtual environment
        cd ~/SoftwareDev/bin/tts
        source .venv/bin/activate
        
        # Check if PyYAML is installed
        if ! python -c "import yaml" 2>/dev/null; then
            echo -e "${RED}PyYAML is not installed. Installing...${NC}"
            pip install PyYAML
        fi
        
        # Check if gtts is installed
        if ! python -c "import gtts" 2>/dev/null; then
            echo -e "${RED}gtts is not installed. Installing...${NC}"
            pip install gtts
        fi
        
        # Check if pyperclip is installed
        if ! python -c "import pyperclip" 2>/dev/null; then
            echo -e "${RED}pyperclip is not installed. Installing...${NC}"
            pip install pyperclip
        fi
        
        # Deactivate the virtual environment
        deactivate
        
        print_step "Testing with direct text input..."
        cd ~/SoftwareDev/bin/tts
        ./speak --text "This is a test of the speak command." --output-only --use-gtts
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Speak command test passed!${NC}"
        else
            echo -e "${RED}✗ Speak command test failed!${NC}"
            echo "Check the error message above for details."
        fi
    else
        echo -e "${RED}✗ Speak command not found!${NC}"
        echo "The speak script was not created properly."
    fi
}

# Main function
main() {
    print_header "Testing Deployment Setup"
    
    # Setup deployment
    setup_deployment
    
    # Test speak command
    test_speak_command
    
    print_header "Deployment Test Complete"
    echo -e "To use the 'speak' command from anywhere, add this to your ~/.zshrc:"
    echo -e "${BLUE}export PATH=\"\$HOME/SoftwareDev/bin/tts:\$PATH\"${NC}"
    echo -e "\nThen restart your terminal or run: ${BLUE}source ~/.zshrc${NC}"
}

# Run the main function
main 