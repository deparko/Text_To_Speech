# Text-to-Speech Application Tests

This directory contains tests for the modular Text-to-Speech application.

## Available Tests

### 1. Main Script Tests

These tests verify that the main script works correctly with different input methods:

- **test_main_script.py**: Python script that tests the main functionality
  - Test 1: Reading from clipboard
  - Test 2: Reading from direct text input
  - Test 3: Reading from a text file

- **test_main_script.sh**: Shell script version of the same tests

### 2. Deployment Test

- **test_deployment.sh**: Tests the deployment setup with the "speak" command
  - Sets up the deployment directory
  - Creates the virtual environment
  - Installs dependencies
  - Creates the "speak" command script
  - Tests the "speak" command

## Running the Tests

### Testing the Main Script

```bash
# Using Python
python tests/test_main_script.py

# Using Shell
./tests/test_main_script.sh
```

### Testing the Deployment

```bash
./tests/test_deployment.sh
```

## What the Tests Verify

1. **Clipboard Functionality**: Tests that the application can read text from the clipboard.
2. **Direct Text Input**: Tests that the application can process text provided directly via the `--text` argument.
3. **File Input**: Tests that the application can read text from files.
4. **Modular Structure**: Verifies that the modular structure works correctly.
5. **Deployment**: Tests that the application can be deployed and run as a command-line tool.

## Notes

- The tests use Google TTS (`--use-gtts`) for faster testing and to avoid dependencies on local TTS models.
- The tests use the `--output-only` flag to avoid playing audio during testing.
- The deployment test creates a virtual environment and installs only the essential dependencies.

## Adding New Tests

To add new tests:

1. Create a new test file in the `tests` directory.
2. Follow the pattern of existing tests.
3. Make sure to clean up any temporary files or resources.
4. Update this README to include the new test. 