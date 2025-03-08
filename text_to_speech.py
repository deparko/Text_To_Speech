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
from pathlib import Path

# Get the script directory
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Add the script directory to the Python path if not already there
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from tts_core.config import Config
from tts_core.input_handler import InputHandler
from tts_core.output_handler import OutputHandler
from tts_core.tts_engine import TTSEngine

def setup_logging():
    """Set up logging configuration."""
    log_dir = SCRIPT_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return log_path

def main():
    """Main entry point for the TTS utility."""
    # Set up logging first
    log_path = setup_logging()
    logging.info(f"Logging to {log_path}")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Convert text to speech using various TTS engines.")
    parser.add_argument("--text", help="Text to convert to speech")
    parser.add_argument("--file", help="File containing text to convert")
    parser.add_argument("--use-gtts", action="store_true", help="Use Google TTS instead of OpenAI")
    parser.add_argument("--use-openai", action="store_true", help="Use OpenAI TTS (default)")
    parser.add_argument("--voice", help="OpenAI voice to use (nova, alloy, echo, fable, onyx, shimmer)")
    parser.add_argument("--speed", type=float, help="Speech speed multiplier")
    parser.add_argument("--no-play", action="store_true", help="Don't play the audio after generation")
    parser.add_argument("--list-voices", action="store_true", help="List available voices/models")
    args = parser.parse_args()
    
    try:
        # Load config from the script directory
        config = Config(SCRIPT_DIR / 'tts_config.yaml')
        logging.info(f"Configuration loaded from {SCRIPT_DIR / 'tts_config.yaml'}")
        
        # Set up handlers
        output_handler = OutputHandler(config)
        input_handler = InputHandler()
        
        # Update config with command line arguments
        if args.use_gtts:
            config.set("model", "use_gtts", True)
            config.set("model", "use_openai", False)
            logging.info("Using Google TTS engine")
        elif args.use_openai:
            config.set("model", "use_gtts", False)
            config.set("model", "use_openai", True)
            logging.info("Using OpenAI TTS engine")
        
        if args.voice:
            config.set("openai", "voice", args.voice)
            logging.info(f"Using OpenAI voice: {args.voice}")
        
        if args.speed:
            config.set("voice", "speed", args.speed)
        
        if args.no_play:
            config.set("output", "play_audio", False)
        
        # Initialize TTS engine after config updates
        tts_engine = TTSEngine(config)
        
        # Handle --list-voices
        if args.list_voices:
            tts_engine.list_voices()
            return
        
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
        format_ext = "mp3"  # Both gTTS and OpenAI use MP3 format
        output_path = output_handler.save_audio(audio_data, format_ext, original_text=text)
        
        if config.get("output", "play_audio", True):
            output_handler.play_audio(output_path)
            
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()