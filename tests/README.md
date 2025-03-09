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

### 3. AI Integration Tests

- **test_ai_integration.py**: Python unit tests for AI Text Processor integration
  - Tests AI filename generation
  - Tests AI text preprocessing
  - Tests error handling
  - Includes mocked tests and real integration tests

- **test_ai_integration.sh**: Shell script for testing AI integration in production
  - Tests listing available AI prompts
  - Tests AI text preprocessing
  - Tests AI filename generation
  - Tests combinations of AI features with other options

- **test_openai_integration.sh**: Shell script for testing OpenAI TTS with AI integration
  - Tests basic OpenAI TTS functionality
  - Tests AI text preprocessing with OpenAI TTS
  - Tests AI filename generation with OpenAI TTS
  - Tests OpenAI voice selection
  - Tests combinations of AI features with OpenAI voices

- **test_openai_tts_with_ai.sh**: Shell script for testing all AI prompts with OpenAI TTS
  - Tests each available AI prompt with OpenAI TTS
  - Verifies compatibility between AI prompts and OpenAI TTS
  - Documents any issues or limitations

## Test Results

- **openai_tts_integration_results.md**: Detailed documentation of OpenAI TTS integration testing
  - Summary of findings and fixes
  - Test results for all AI prompts with OpenAI TTS
  - Recommendations for users and developers
  - Next steps for improving the integration

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

### Testing the AI Integration

```bash
# Using Python (unit tests)
python -m unittest tests/test_ai_integration.py

# Using Shell (production tests with Google TTS)
./tests/test_ai_integration.sh

# Using Shell (production tests with OpenAI TTS)
./tests/test_openai_integration.sh
```

## What the Tests Verify

1. **Clipboard Functionality**: Tests that the application can read text from the clipboard.
2. **Direct Text Input**: Tests that the application can process text provided directly via the `--text` argument.
3. **File Input**: Tests that the application can read text from files.
4. **Modular Structure**: Verifies that the modular structure works correctly.
5. **Deployment**: Tests that the application can be deployed and run as a command-line tool.
6. **AI Integration**: Tests the integration with the AI Text Processor:
   - AI-powered text preprocessing
   - Smart filename generation
   - Error handling and fallbacks

## Notes

- The tests use Google TTS (`--use-gtts`) for faster testing and to avoid dependencies on local TTS models.
- The tests use the `--output-only` flag to avoid playing audio during testing.
- The deployment test creates a virtual environment and installs only the essential dependencies.
- The AI integration tests require the AI Text Processor to be installed and configured.
- Some tests require an OpenAI API key to be set in the environment.

## Adding New Tests

To add new tests:

1. Create a new test file in the `tests` directory.
2. Follow the pattern of existing tests.
3. Make sure to clean up any temporary files or resources.
4. Update this README to include the new test. 