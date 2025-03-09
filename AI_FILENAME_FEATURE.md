# AI-Generated Filenames Feature

This document describes the AI-generated filenames feature for the Text-to-Speech (TTS) system.

## Overview

The AI-generated filenames feature uses the AI Text Processor to create descriptive filenames for your TTS audio files based on the content of the text. Instead of generic timestamp-based filenames like `tts_20250308_224512.wav`, you'll get meaningful filenames like `climate_change_report_20250308_224512.wav`.

## Requirements

- The AI Text Processor must be installed in one of these locations:
  - `~/SoftwareDev/AI-Text-Processor/`
  - `~/SoftwareDev/bin/AI-Text-Processor/`

## Usage

### Basic Usage

By default, AI-generated filenames are enabled. Simply use the `speak` command as usual:

```bash
speak --text "Climate change is accelerating at an alarming rate, according to a new UN report."
```

This will generate a file with a name like `climate_change_accelerating_20250308_224512.wav`.

### Disabling AI Filenames

If you prefer the traditional timestamp-based filenames, use the `--no-ai-filename` flag:

```bash
speak --text "Hello world" --no-ai-filename
```

This will generate a file with a name like `tts_20250308_224512.wav`.

### Using Specific Prompts

You can choose which AI prompt to use for generating the filename. Different prompts will produce different results:

```bash
speak --text "Climate change is accelerating at an alarming rate." --ai-summarize
```

To see all available prompts:

```bash
speak --list-ai-prompts
```

## Available Prompts

The following prompts are available for filename generation:

- `summarize`: Creates a concise summary (default)
- `simplify`: Simplifies complex text
- `general_cleanup`: Cleans up text while preserving meaning
- `cleanup_for_tts`: Formats text for optimal TTS conversion
- `enhance_for_tts`: Improves text flow for speech
- And more, depending on your AI Text Processor configuration

## How It Works

1. The TTS system sends the input text to the AI Text Processor
2. The AI Text Processor applies the selected prompt to generate a summary
3. The summary is processed to create a filename:
   - Special characters are removed
   - Text is converted to lowercase
   - The first 3 words are selected
   - Words are joined with underscores
   - A timestamp is appended

## Troubleshooting

If AI-generated filenames are not working:

1. Make sure the AI Text Processor is installed in one of the expected locations
2. Check that the AI Text Processor is working correctly by running it directly
3. Look for error messages in the TTS log file
4. Try using a specific prompt with the `--ai-<prompt>` flag

## Examples

| Input Text | Generated Filename |
|------------|-------------------|
| "Climate change is accelerating at an alarming rate." | `climate_change_accelerating_20250308_224512.wav` |
| "The meeting with Dr. Smith is scheduled for tomorrow." | `meeting_with_dr_20250308_224512.wav` |
| "Python is a programming language that lets you work quickly and integrate systems more effectively." | `python_programming_language_20250308_224512.wav` | 