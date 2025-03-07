#!/bin/bash
# Test the main Text-to-Speech script with different input methods

# Change to the parent directory where the main script is located
cd "$(dirname "$0")/.."
MAIN_SCRIPT="$(pwd)/text_to_speech.py"

# Set output-only flag to avoid playing audio during tests
OUTPUT_ONLY="--output-only"

# Use Google TTS for faster testing
USE_GTTS="--use-gtts"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print section header
print_header() {
    echo -e "\n${YELLOW}=======================================${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${YELLOW}=======================================${NC}"
}

# Function to run a test and check result
run_test() {
    local test_name="$1"
    local command="$2"
    
    echo -e "\n${YELLOW}Testing: ${test_name}${NC}"
    echo -e "Command: ${command}"
    
    # Run the command
    eval $command
    
    # Check result
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Test passed: ${test_name}${NC}"
        return 0
    else
        echo -e "${RED}✗ Test failed: ${test_name}${NC}"
        return 1
    fi
}

# Create a temporary text file for testing
create_test_file() {
    local temp_file=$(mktemp)
    echo "This is a test file for the Text-to-Speech application." > "$temp_file"
    echo "$temp_file"
}

# Main test function
main() {
    print_header "Testing Text-to-Speech Main Script"
    
    # Test 1: Reading from clipboard
    print_header "Test 1: Reading from clipboard"
    echo "Setting clipboard content..."
    echo "This is a test of reading from the clipboard." | pbcopy
    run_test "Reading from clipboard" "python $MAIN_SCRIPT $OUTPUT_ONLY $USE_GTTS"
    
    # Test 2: Reading from direct text input
    print_header "Test 2: Reading from direct text input"
    run_test "Reading from direct text input" "python $MAIN_SCRIPT --text \"This is a test of reading from direct text input.\" $OUTPUT_ONLY $USE_GTTS"
    
    # Test 3: Reading from a text file
    print_header "Test 3: Reading from a text file"
    temp_file=$(create_test_file)
    run_test "Reading from a text file" "python $MAIN_SCRIPT --file \"$temp_file\" $OUTPUT_ONLY $USE_GTTS"
    rm -f "$temp_file"
    
    print_header "All tests completed"
}

# Run the tests
main 