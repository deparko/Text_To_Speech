#!/bin/bash
# Script to create a speak alias in your .zshrc file

# Check if .zshrc exists
if [ ! -f "$HOME/.zshrc" ]; then
    echo "Error: $HOME/.zshrc does not exist"
    exit 1
fi

# Add the alias to .zshrc if it doesn't already exist
if ! grep -q "alias speak=" "$HOME/.zshrc"; then
    echo "" >> "$HOME/.zshrc"
    echo "# Alias for the speak command to handle quotes properly" >> "$HOME/.zshrc"
    echo "alias speak='~/SoftwareDev/bin/tts/speak'" >> "$HOME/.zshrc"
    echo "Added speak alias to $HOME/.zshrc"
    echo "Please restart your shell or run 'source ~/.zshrc' to apply the changes"
else
    echo "speak alias already exists in $HOME/.zshrc"
fi

echo ""
echo "After applying the changes, you can use the speak command like this:"
echo "speak --text 'Hello World!'"
echo "or"
echo "speak --text \"Hello World!\"" 