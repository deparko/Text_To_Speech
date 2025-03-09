# Manual Test Cases for TTS System

This document provides a set of manual test cases you can run in the terminal to verify the functionality of the TTS system with OpenAI TTS and AI Text Processor integration.

## Prerequisites

1. Make sure you have deployed the latest version to the bin directory:
   ```bash
   cd ~/SoftwareDev/Text_To_Speech && ./deploy_to_bin.sh
   ```

2. Make sure the integrated environment is set up:
   ```bash
   cd ~/SoftwareDev/bin/tts && ./setup_integrated_env.sh
   ```

3. Ensure your OpenAI API key is properly configured in `tts_config.yaml`.

## Basic Functionality Tests

### Test Case 1: Basic OpenAI TTS

```bash
cd ~/SoftwareDev/bin/tts && ./speak --text 'This is a test of OpenAI TTS.' --no-play
```

**Expected Result**: Audio file should be generated without errors.

### Test Case 2: Google TTS

```bash
cd ~/SoftwareDev/bin/tts && ./speak --text 'This is a test of Google TTS.' --use-gtts --no-play
```

**Expected Result**: Audio file should be generated using Google TTS without errors.

### Test Case 3: Different OpenAI Voices

```bash
cd ~/SoftwareDev/bin/tts && ./speak --text 'This is a test of different OpenAI voices.' --voice alloy --no-play
```

**Expected Result**: Audio file should be generated using the specified voice (alloy) without errors.

## AI Text Processor Integration Tests

### Test Case 4: List Available AI Prompts

```bash
cd ~/SoftwareDev/bin/tts && ./speak --list-ai-prompts
```

**Expected Result**: A list of available AI prompts should be displayed.

### Test Case 5: AI Text Preprocessing with OpenAI TTS

```bash
cd ~/SoftwareDev/bin/tts && ./speak --text 'On 4/15/2023, Dr. Smith met with 3 patients at 123 Main St.' --ai-cleanup_for_tts --no-play
```

**Expected Result**: Text should be preprocessed to expand numbers, abbreviations, etc., and audio should be generated without errors.

### Test Case 6: AI Text Preprocessing with Google TTS

```bash
cd ~/SoftwareDev/bin/tts && ./speak --text 'On 4/15/2023, Dr. Smith met with 3 patients at 123 Main St.' --ai-cleanup_for_tts --use-gtts --no-play
```

**Expected Result**: Text should be preprocessed and audio should be generated using Google TTS without errors.

### Test Case 7: AI Filename Generation

```bash
cd ~/SoftwareDev/bin/tts && ./speak --text 'The mitochondria is the powerhouse of the cell' --ai-summarize --use-gtts --no-play
```

**Expected Result**: A descriptive filename should be generated based on the content.

## File Input Tests

### Test Case 8: File Input with AI Preprocessing

```bash
echo "Complex scientific text with abbreviations: The DNA and RNA are nucleic acids." > /tmp/test_input.txt
cd ~/SoftwareDev/bin/tts && ./speak --file /tmp/test_input.txt --ai-expand --no-play
```

**Expected Result**: Text from the file should be preprocessed and audio should be generated without errors.

## Clipboard Input Tests

### Test Case 9: Clipboard Input

```bash
# First, copy some text to the clipboard, then run:
cd ~/SoftwareDev/bin/tts && ./speak --no-play
```

**Expected Result**: Text from the clipboard should be processed and audio should be generated without errors.

## Running from Any Directory

### Test Case 10: Running from Any Directory

```bash
# Add the bin/tts directory to your PATH (temporary for this session)
export PATH=$PATH:~/SoftwareDev/bin/tts

# Now you can run the speak command from any directory
cd /tmp && speak --text 'Testing running from any directory' --no-play
```

**Expected Result**: The command should work from any directory.

## Testing All AI Prompts

### Test Case 11: Testing All AI Prompts with OpenAI TTS

```bash
cd ~/SoftwareDev/bin/tts && ./tests/test_openai_tts_with_ai.sh
```

**Expected Result**: All AI prompts should be tested with OpenAI TTS, and the results should be displayed.

## Testing OpenAI TTS Integration

### Test Case 12: Testing OpenAI TTS Integration

```bash
cd ~/SoftwareDev/bin/tts && ./tests/test_openai_integration.sh
```

**Expected Result**: The OpenAI TTS integration tests should run and pass.

## Troubleshooting Tests

### Test Case 13: Check AI Text Processor Availability

```bash
cd ~/SoftwareDev/bin/tts && ls -la AI-Text-Processor
```

**Expected Result**: The symbolic link to the AI Text Processor should exist.

### Test Case 14: Test AI Text Processor Directly

```bash
cd ~/SoftwareDev/AI-Text-Processor && python examples/cli.py --text 'Test text' --prompt simplify
```

**Expected Result**: The AI Text Processor should process the text and return a simplified version.

## Notes

- If you encounter any errors, check the logs for more information.
- For tests with `--no-play`, you can remove this flag to play the audio after generation.
- If you want to see the generated files, check your configured output directory (default is `~/tts_output`).
- **Important**: Always use single quotes around text arguments to avoid shell interpretation issues.
- Some complex texts may cause issues with OpenAI TTS when using AI prompts. If you encounter errors, try using Google TTS instead by adding the `--use-gtts` flag. 