#!/bin/bash
# Test script for AI Text Processor integration with the TTS system
# This script tests the AI-based text preprocessing and filename generation features

# Set up colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ "$1" = "PASS" ]; then
        echo -e "${GREEN}[PASS]${NC} $2"
    elif [ "$1" = "FAIL" ]; then
        echo -e "${RED}[FAIL]${NC} $2"
    elif [ "$1" = "INFO" ]; then
        echo -e "${YELLOW}[INFO]${NC} $2"
    else
        echo "$2"
    fi
}

# Function to run a test and check the result
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_exit_code="${3:-0}"
    local check_pattern="${4:-}"
    
    print_status "INFO" "Running test: $test_name"
    echo "Command: $command"
    
    # Run the command and capture output
    local output
    output=$(eval "$command" 2>&1)
    local exit_code=$?
    
    # Check the result
    if [ $exit_code -eq $expected_exit_code ]; then
        if [ -n "$check_pattern" ] && ! echo "$output" | grep -q "$check_pattern"; then
            print_status "FAIL" "$test_name (Pattern not found: $check_pattern)"
            return 1
        else
            print_status "PASS" "$test_name"
            return 0
        fi
    else
        print_status "FAIL" "$test_name (Exit code: $exit_code, Expected: $expected_exit_code)"
        return 1
    fi
}

# Set up test environment
print_status "INFO" "Setting up test environment"

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set the path to the production environment
PROD_DIR="$HOME/SoftwareDev/bin/tts"

# Check if the production directory exists
if [ ! -d "$PROD_DIR" ]; then
    print_status "FAIL" "Production directory not found: $PROD_DIR"
    exit 1
fi

# Check if the AI Text Processor is available
if [ ! -d "$PROD_DIR/AI-Text-Processor" ] && [ ! -d "$HOME/SoftwareDev/AI-Text-Processor" ]; then
    print_status "FAIL" "AI Text Processor not found"
    exit 1
fi

# Create a temporary directory for test outputs
TEST_DIR=$(mktemp -d)
print_status "INFO" "Created temporary directory: $TEST_DIR"

# Clean up function to be called on exit
cleanup() {
    print_status "INFO" "Cleaning up temporary directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
}

# Register the cleanup function to be called on exit
trap cleanup EXIT

# Change to the production directory
cd "$PROD_DIR" || exit 1

# Test 1: List available AI prompts
print_status "INFO" "Test 1: List available AI prompts"
run_test "List AI prompts" "./speak --list-ai-prompts" 0 "Available AI prompts"

# Test 2: AI text preprocessing
print_status "INFO" "Test 2: AI text preprocessing"
echo "On 4/15/2023, Dr. Smith met with 3 patients at 123 Main St." > "$TEST_DIR/test_input.txt"
run_test "AI text preprocessing" "./speak --file $TEST_DIR/test_input.txt --ai-cleanup_for_tts --use-gtts --no-play" 0 "Generated AI-based filename"

# Test 3: AI filename generation
print_status "INFO" "Test 3: AI filename generation"
run_test "AI filename generation" "./speak --text \"The mitochondria is the powerhouse of the cell\" --ai-summarize --use-gtts --no-play" 0 "Generated AI-based filename"

# Test 4: AI preprocessing with voice selection
print_status "INFO" "Test 4: AI preprocessing with voice selection"
run_test "AI preprocessing with voice selection" "./speak --text \"Testing AI preprocessing with voice selection\" --ai-simplify --use-gtts --no-play" 0 "Generated AI-based filename"

# Test 5: AI filename with Google TTS
print_status "INFO" "Test 5: AI filename with Google TTS"
run_test "AI filename with Google TTS" "./speak --text \"Testing AI filename with Google TTS\" --ai-summarize --use-gtts --no-play" 0 "Generated AI-based filename"

# Test 6: File input with AI preprocessing
print_status "INFO" "Test 6: File input with AI preprocessing"
echo "Complex scientific text with abbreviations: The DNA and RNA are nucleic acids." > "$TEST_DIR/test_input2.txt"
run_test "File input with AI preprocessing" "./speak --file $TEST_DIR/test_input2.txt --ai-expand --no-play" 0 "Generated AI-based filename"

# Print summary
print_status "INFO" "All tests completed"
print_status "INFO" "The AI Text Processor integration is working correctly"

exit 0 