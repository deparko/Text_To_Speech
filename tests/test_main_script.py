#!/usr/bin/env python3
"""
Test script for the Text-to-Speech application.
This script tests the main functionality by executing the main script with different input methods.
"""

import os
import sys
import tempfile
import subprocess
import pyperclip
from pathlib import Path

# Get the path to the main script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(os.path.dirname(SCRIPT_DIR), "text_to_speech.py")

# Set output-only flag to avoid playing audio during tests
OUTPUT_ONLY = "--output-only"

# Use Google TTS for faster testing
USE_GTTS = "--use-gtts"

def print_header(title):
    """Print a section header."""
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

def run_test(test_name, command):
    """Run a test and check the result."""
    print(f"\nTesting: {test_name}")
    print(f"Command: {' '.join(command)}")
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Check result
    if result.returncode == 0:
        print(f"✅ Test passed: {test_name}")
        return True
    else:
        print(f"❌ Test failed: {test_name}")
        print(f"Error: {result.stderr}")
        return False

def create_test_file():
    """Create a temporary text file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w') as f:
        f.write("This is a test file for the Text-to-Speech application.")
        return f.name

def main():
    """Run the tests."""
    print_header("Testing Text-to-Speech Main Script")
    
    # Save original clipboard content
    original_clipboard = pyperclip.paste()
    
    try:
        # Test 1: Reading from clipboard
        print_header("Test 1: Reading from clipboard")
        print("Setting clipboard content...")
        pyperclip.copy("This is a test of reading from the clipboard.")
        run_test("Reading from clipboard", 
                [sys.executable, MAIN_SCRIPT, OUTPUT_ONLY, USE_GTTS])
        
        # Test 2: Reading from direct text input
        print_header("Test 2: Reading from direct text input")
        run_test("Reading from direct text input", 
                [sys.executable, MAIN_SCRIPT, "--text", 
                "This is a test of reading from direct text input.", 
                OUTPUT_ONLY, USE_GTTS])
        
        # Test 3: Reading from a text file
        print_header("Test 3: Reading from a text file")
        temp_file = create_test_file()
        run_test("Reading from a text file", 
                [sys.executable, MAIN_SCRIPT, "--file", temp_file, 
                OUTPUT_ONLY, USE_GTTS])
        os.unlink(temp_file)
        
        print_header("All tests completed")
    finally:
        # Restore original clipboard content
        pyperclip.copy(original_clipboard)

if __name__ == "__main__":
    main() 