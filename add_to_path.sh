#!/bin/bash
# Script to add the TTS system to the PATH

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set the target directory
TARGET_DIR="$HOME/SoftwareDev/bin/tts"

# Check if the target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory $TARGET_DIR does not exist"
    echo "Please run ./deploy_to_bin.sh first"
    exit 1
fi

# Check which shell the user is using
SHELL_NAME=$(basename "$SHELL")

# Add the target directory to the PATH in the appropriate shell configuration file
if [ "$SHELL_NAME" = "bash" ]; then
    CONFIG_FILE="$HOME/.bashrc"
    echo "Adding to $CONFIG_FILE"
    if ! grep -q "export PATH=\$PATH:$TARGET_DIR" "$CONFIG_FILE"; then
        echo "" >> "$CONFIG_FILE"
        echo "# Add TTS system to PATH" >> "$CONFIG_FILE"
        echo "export PATH=\$PATH:$TARGET_DIR" >> "$CONFIG_FILE"
    fi
elif [ "$SHELL_NAME" = "zsh" ]; then
    CONFIG_FILE="$HOME/.zshrc"
    echo "Adding to $CONFIG_FILE"
    if ! grep -q "export PATH=\$PATH:$TARGET_DIR" "$CONFIG_FILE"; then
        echo "" >> "$CONFIG_FILE"
        echo "# Add TTS system to PATH" >> "$CONFIG_FILE"
        echo "export PATH=\$PATH:$TARGET_DIR" >> "$CONFIG_FILE"
    fi
else
    echo "Unsupported shell: $SHELL_NAME"
    echo "Please manually add the following line to your shell configuration file:"
    echo "export PATH=\$PATH:$TARGET_DIR"
    exit 1
fi

echo "Added $TARGET_DIR to PATH in $CONFIG_FILE"
echo "Please restart your shell or run 'source $CONFIG_FILE' to apply the changes"
echo ""
echo "After that, you can run the 'speak' command from any directory"
echo "For example: speak --text \"Hello, world!\"" 