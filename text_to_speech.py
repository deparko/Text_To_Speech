#!/usr/bin/env python3
"""
Text-to-Speech Clipboard Utility
Converts text to speech using various TTS engines.
"""

import os
import sys
import logging
import argparse
from datetime import datetime

from tts_core.config import Config
from tts_core.input_handler import InputHandler
from tts_core.output_handler import OutputHandler
from tts_core.tts_engine import TTSEngine

def setup_logging(log_path):
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main entry point for the TTS utility."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Convert text to speech using various TTS engines.")
    parser.add_argument("--text", help="Text to convert to speech")
    parser.add_argument("--file", help="File containing text to convert")
    parser.add_argument("--use-gtts", action="store_true", help="Use Google TTS instead of local model")
    parser.add_argument("--speed", type=float, help="Speech speed multiplier")
    parser.add_argument("--no-play", action="store_true", help="Don't play the audio after generation")
    parser.add_argument("--list-voices", action="store_true", help="List available voices/models")
    args = parser.parse_args()
    
    # Load configuration
    config = Config()
    
    # Set up handlers
    output_handler = OutputHandler(config)
    input_handler = InputHandler()
    tts_engine = TTSEngine(config)
    
    # Set up logging
    log_path = output_handler.get_log_path()
    setup_logging(log_path)
    
    # Log configuration source
    logging.info(f"Configuration loaded from {os.path.abspath('tts_config.yaml')}")
    
    # Handle --list-voices
    if args.list_voices:
        tts_engine.list_voices()
        return
    
    # Update config with command line arguments
    if args.use_gtts:
        config.set("model", "use_gtts", True)
        logging.info("Using Google TTS engine")
    
    if args.speed:
        config.set("voice", "speed", args.speed)
    
    if args.no_play:
        config.set("output", "play_audio", False)
    
    # Get input text
    text = None
    if args.text:
        text = args.text
    elif args.file:
        text = input_handler.from_file(args.file)
    else:
        text = input_handler.from_clipboard()
        
    if not text:
        logging.error("No text provided")
        return
    
    # Clean the text
    text = input_handler.clean_text(text)
    logging.info(f"Using provided text ({len(text)} characters)")
    
    # Generate speech
    audio_data = tts_engine.generate_speech(text)
    if not audio_data:
        logging.error("Failed to generate speech")
        return
    
    # Save and play audio
    format_ext = "mp3" if config.get("model", "use_gtts", False) else "wav"
    output_path = output_handler.save_audio(audio_data, format_ext)
    
    if config.get("output", "play_audio", True):
        output_handler.play_audio(output_path)

if __name__ == "__main__":
    main()