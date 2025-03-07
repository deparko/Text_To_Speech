#!/bin/bash

# Test script for macOS integration
# This script tests the podcast integration in a real macOS environment

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name=$1
    local command=$2
    
    echo "Running test: $test_name"
    echo "Command: $command"
    
    if eval "$command"; then
        echo -e "${GREEN}✓ Test passed: $test_name${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ Test failed: $test_name${NC}"
        ((TESTS_FAILED++))
    fi
    echo "----------------------------------------"
}

# Ensure we're in the right directory
cd "$(dirname "$0")/.." || exit 1

# Create test directories
TEST_DIR="$HOME/Documents/TTS_Test"
mkdir -p "$TEST_DIR"
TEST_AUDIO="$TEST_DIR/test_audio"
TEST_PODCAST="$TEST_DIR/test_podcast"

# Create test config
cat > "$TEST_DIR/test_config.yaml" << EOL
model:
  name: "tts_models/en/ljspeech/tacotron2-DDC"
  use_gtts: true

voice:
  speed: 1.0
  speaker_id: null
  pitch: null

output:
  folder: "$TEST_AUDIO"
  play_audio: false
  cache_audio: false

podcast:
  enabled: true
  folder: "$TEST_PODCAST"
  title: "Test TTS Podcast"
  description: "Test podcast feed"
  author: "Test Author"
  add_to_itunes: true
EOL

echo "Starting macOS integration tests..."

# Test 1: Basic TTS with podcast disabled
run_test "Basic TTS" "./speak --text 'This is a test' --config '$TEST_DIR/test_config.yaml' --no-podcast"

# Test 2: Enable podcast for single run
run_test "Single podcast episode" "./speak --text 'This is a podcast test' --config '$TEST_DIR/test_config.yaml' --enable-podcast --podcast-title 'Test Episode'"

# Test 3: Check RSS feed creation
run_test "RSS feed check" "test -f '$TEST_PODCAST/feed.xml'"

# Test 4: Multiple episodes
run_test "Multiple episodes" "
./speak --text 'Episode one' --config '$TEST_DIR/test_config.yaml' --enable-podcast --podcast-title 'Episode 1' &&
./speak --text 'Episode two' --config '$TEST_DIR/test_config.yaml' --enable-podcast --podcast-title 'Episode 2'
"

# Test 5: iTunes integration
run_test "iTunes integration" "osascript -e 'tell application \"Music\" to get name of playlists' | grep 'Library'"

# Test 6: Check podcast folder structure
run_test "Folder structure" "
test -d '$TEST_PODCAST' &&
test -f '$TEST_PODCAST/feed.xml' &&
ls '$TEST_PODCAST' | grep -q '\.mp3'
"

# Clean up
echo "Cleaning up test files..."
rm -rf "$TEST_DIR"

# Print results
echo "----------------------------------------"
echo "Test Results:"
echo -e "${GREEN}Tests passed: $TESTS_PASSED${NC}"
echo -e "${RED}Tests failed: $TESTS_FAILED${NC}"
echo "----------------------------------------"

# Exit with status based on test results
[ "$TESTS_FAILED" -eq 0 ] 