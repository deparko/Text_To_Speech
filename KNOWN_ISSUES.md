# Known Issues and Limitations

## Text Processing

1. **Long Text Handling**
   - Very long texts (>10,000 characters) may need to be split into multiple requests
   - Current segmentation might split sentences at suboptimal points
   - Quote detection might fail for nested quotes

2. **Special Characters**
   - Some Unicode characters may not be properly handled
   - Emojis and special symbols are stripped from text
   - Non-English characters might affect timing calculations

3. **Formatting**
   - Markdown formatting in input text is treated as plain text
   - HTML tags in input text are not stripped
   - Code blocks may not be properly segmented

## Audio Generation

1. **OpenAI TTS**
   - API rate limits may affect processing of long texts
   - Occasional connection timeouts require retry logic
   - Voice emotion/style cannot be controlled directly

2. **Google TTS (gTTS)**
   - Less natural voice quality compared to OpenAI
   - Limited control over voice characteristics
   - Network issues may cause generation failures

3. **Audio Timing**
   - Character-based timing estimation may be inaccurate
   - Segment durations might not match actual speech duration
   - Speed adjustments may affect timing calculations

## Output Files

1. **HTML Viewer**
   - Audio seeking might be slightly inaccurate
   - Auto-scroll may jump too early/late
   - Requires local file access for audio playback
   - Relative paths might break if files are moved

2. **Markdown Files**
   - Links to audio files are relative and may break if moved
   - Table of contents might be too long for very long texts
   - Timestamp calculations are estimates

3. **SRT Files**
   - Timing may not perfectly match audio
   - Limited formatting options
   - No support for styling or positioning

## System Integration

1. **iCloud Integration**
   - Files may take time to sync across devices
   - Large files might cause sync issues
   - Cache management needs improvement

2. **File Management**
   - No automatic cleanup of old files
   - Cache size can grow indefinitely
   - No file organization by date/type

3. **Playback**
   - System audio player may not support all features
   - No volume normalization
   - No audio effects or post-processing

## Development

1. **Testing**
   - Limited test coverage for edge cases
   - No automated UI tests for HTML viewer
   - Mock API responses needed for offline testing

2. **Dependencies**
   - Python 3.10+ requirement may be too restrictive
   - ffmpeg dependency needs better error handling
   - Package versions need regular updates

3. **Documentation**
   - API documentation needs improvement
   - Code comments could be more detailed
   - Setup instructions may need clarification

## Planned Solutions

Many of these issues are tracked in [ENHANCEMENTS.md](ENHANCEMENTS.md) with proposed solutions:

1. **Text Processing**
   - Implement smarter text segmentation
   - Add support for markdown parsing
   - Improve quote detection

2. **Audio Generation**
   - Add retry logic for API calls
   - Implement better error handling
   - Add support for more TTS engines

3. **Output Files**
   - Improve timing accuracy
   - Add file organization features
   - Enhance HTML viewer functionality

4. **System Integration**
   - Add file cleanup options
   - Improve cache management
   - Add better sync status indicators

## Reporting Issues

If you encounter any issues not listed here, please:
1. Check the latest version
2. Search existing issues
3. Provide detailed reproduction steps
4. Include relevant logs and system information

## Active Issues

### Text Chunking (High Priority)
- [ ] Need comprehensive testing of text chunking with various lengths
- [ ] Verify audio segment combination for smooth transitions
- [ ] Add error handling for failed chunk processing
- [ ] Make chunk size configurable in tts_config.yaml
- [ ] Add progress tracking for multi-chunk processing

### Coqui TTS Integration (High Priority)
- [ ] Implement proper model download and caching
- [ ] Add voice selection support for Coqui models
- [ ] Handle GPU/CPU detection and selection
- [ ] Add proper error handling for model loading failures
- [ ] Implement fallback mechanism if model download fails
- [ ] Add progress tracking for model downloads
- [ ] Document system requirements for different models
- [ ] Add model configuration options to tts_config.yaml

### Logging System (Medium Priority)
- [ ] Add detailed logging for text chunking process
- [ ] Include chunk size information in logs
- [ ] Add performance timing metrics
- [ ] Consider log rotation for long-term use

### Error Handling (High Priority)
- [ ] Implement proper handling of API rate limiting
- [ ] Add robust network connectivity error handling
- [ ] Improve invalid audio file handling
- [ ] Add retry mechanism for failed API calls
- [ ] Handle Coqui TTS specific errors and exceptions

### Configuration Management (Medium Priority)
- [ ] Ensure consistent config synchronization between dev and deployment
- [ ] Add more configurable options for chunking feature
- [ ] Document all configuration options
- [ ] Add validation for configuration values
- [ ] Add Coqui TTS specific configuration options

## Resolved Issues
*(Move items here when fixed)*

## Contributing
When adding new issues:
1. Add a clear description of the issue
2. Assign a priority (High/Medium/Low)
3. Add any relevant error messages or logs
4. Link to relevant code files if applicable

## Issue Template
```markdown
### Issue Title
- **Priority:** [High/Medium/Low]
- **Status:** [Active/In Progress/Resolved]
- **Description:** Brief description of the issue
- **Related Files:** List of related files
- **Error Messages:** Any relevant error messages
- **Notes:** Additional context or notes
``` 