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
from tts_core.ai_filename_generator import AIFilenameGenerator

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

def add_ai_prompt_arguments(parser, ai_generator):
    """
    Add AI prompt arguments to the parser.
    
    Args:
        parser: ArgumentParser instance
        ai_generator: AIFilenameGenerator instance
    """
    available_prompts = ai_generator.get_available_prompts()
    for prompt in available_prompts:
        parser.add_argument(
            f"--ai-{prompt}", 
            action="store_true",
            help=f"Use '{prompt}' prompt for AI filename generation"
        )

def main():
    """Main entry point for the TTS utility."""
    # Set up logging first
    log_path = setup_logging()
    logging.info(f"Logging to {log_path}")
    
    # Load config first to initialize AI generator for prompt discovery
    config = Config(SCRIPT_DIR / 'tts_config.yaml')
    logging.info(f"Configuration loaded from {SCRIPT_DIR / 'tts_config.yaml'}")
    
    # Initialize AI filename generator for prompt discovery
    ai_generator = AIFilenameGenerator(config)
    
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
    
    # Add AI filename generation arguments
    parser.add_argument("--no-ai-filename", action="store_true", help="Disable AI-generated filenames")
    parser.add_argument("--list-ai-prompts", action="store_true", help="List available AI prompts for filename generation")
    
    # Dynamically add AI prompt arguments
    add_ai_prompt_arguments(parser, ai_generator)
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Set up handlers
        output_handler = OutputHandler(config)
        input_handler = InputHandler()
        
        # Handle --list-ai-prompts
        if args.list_ai_prompts:
            prompts = ai_generator.get_available_prompts()
            if prompts:
                print("Available AI prompts for filename generation:")
                for prompt in prompts:
                    print(f"  --ai-{prompt}")
                print("\nUse with: speak --ai-<prompt_name>")
            else:
                print("No AI prompts available. Make sure the AI Text Processor is installed.")
            return
        
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
        
        # Determine which AI prompt to use for filename generation
        ai_filename = not args.no_ai_filename
        prompt_name = None
        original_text = text  # Store the original text
        
        # Check for AI prompt arguments
        if ai_filename:
            available_prompts = ai_generator.get_available_prompts()
            
            # Check if any specific prompt was requested
            for prompt in available_prompts:
                arg_name = f"ai_{prompt}"
                # Convert hyphens to underscores for argparse compatibility
                arg_name = arg_name.replace('-', '_')
                if hasattr(args, arg_name) and getattr(args, arg_name):
                    prompt_name = prompt
                    logging.info(f"Using AI prompt '{prompt}' for text processing and filename generation")
                    
                    # Process the text with the AI prompt
                    processed_text = ai_generator.process_text(text, prompt)
                    if processed_text:
                        text = processed_text
                        logging.info(f"Text processed with AI prompt '{prompt}'")
                    else:
                        logging.warning(f"Failed to process text with AI prompt '{prompt}', using original text")
                    
                    break
        
        # Generate speech
        audio_data = tts_engine.generate_speech(text)
        if not audio_data:
            logging.error("Failed to generate speech")
            return
        
        # Save and play audio
        format_ext = "mp3"  # Both gTTS and OpenAI use MP3 format
        output_path = output_handler.save_audio(
            audio_data, 
            format_ext, 
            original_text=original_text,  # Use original text for metadata
            processed_text=text if text != original_text else None,  # Include processed text if different
            ai_filename=ai_filename,
            prompt_name=prompt_name
        )
        
        if config.get("output", "play_audio", True):
            output_handler.play_audio(output_path)
            
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()