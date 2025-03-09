"""
AI-based filename generation for the Text-to-Speech application.
This module handles generating descriptive filenames using AI.
"""

import os
import re
import sys
import logging
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

class AIFilenameGenerator:
    """Generates descriptive filenames using AI text processing."""
    
    def __init__(self, config=None):
        """
        Initialize the AI filename generator.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.default_prompt = "summarize"
        self.max_words = 3
        self.ai_processor_path = self._find_ai_processor()
        
    def _find_ai_processor(self) -> Optional[Path]:
        """
        Find the AI Text Processor CLI script.
        
        Returns:
            Path to the AI Text Processor CLI script, or None if not found
        """
        # Check common locations
        possible_paths = [
            # Direct path in SoftwareDev
            Path(os.path.expanduser("~/SoftwareDev/AI-Text-Processor/examples/cli.py")),
            # Relative to script directory
            Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parent / "AI-Text-Processor" / "examples" / "cli.py",
            # In bin directory
            Path(os.path.expanduser("~/SoftwareDev/bin/AI-Text-Processor/examples/cli.py")),
        ]
        
        for path in possible_paths:
            if path.exists():
                logging.info(f"Found AI Text Processor at {path}")
                return path
                
        logging.warning("AI Text Processor not found. AI filename generation will be disabled.")
        return None
    
    def get_available_prompts(self) -> List[str]:
        """
        Get a list of available prompts from the AI Text Processor.
        
        Returns:
            List of prompt names
        """
        if not self.ai_processor_path:
            return []
            
        try:
            result = subprocess.run(
                [sys.executable, str(self.ai_processor_path), "--list-prompts"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the output to extract prompt names
            prompts = []
            for line in result.stdout.splitlines():
                if ':' in line and not line.startswith('Available prompts'):
                    prompt_name = line.split(':', 1)[0].strip()
                    prompts.append(prompt_name)
            
            return prompts
        except Exception as e:
            logging.error(f"Error getting available prompts: {e}")
            return []
    
    def process_text(self, text: str, prompt_name: str) -> Optional[str]:
        """
        Process text using the AI Text Processor with the specified prompt.
        
        Args:
            text: The text to process
            prompt_name: The name of the prompt to use
            
        Returns:
            The processed text, or None if processing fails
        """
        if not self.ai_processor_path or not text:
            logging.warning("AI Text Processor not available or no text provided")
            return None
            
        try:
            # Create a temporary file with the text
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
                temp.write(text)
                temp_path = temp.name
                
            # Run the AI Text Processor
            cmd = [
                sys.executable,
                str(self.ai_processor_path),
                "--file", temp_path,
                "--prompt", prompt_name
            ]
            
            logging.info(f"Processing text with AI prompt: {prompt_name}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            os.unlink(temp_path)  # Clean up temp file
            
            if result.returncode != 0:
                logging.warning(f"AI Text Processor failed: {result.stderr}")
                return None
                
            # Return the processed text
            processed_text = result.stdout.strip()
            logging.info(f"Text processed with AI prompt '{prompt_name}' (original: {len(text)} chars, processed: {len(processed_text)} chars)")
            return processed_text
            
        except Exception as e:
            logging.error(f"Error processing text with AI: {e}")
            return None
    
    def generate_filename(self, text: str, prompt_name: Optional[str] = None, 
                         max_words: Optional[int] = None) -> str:
        """
        Generate a descriptive filename based on text content.
        
        Args:
            text: The text to process
            prompt_name: The name of the prompt to use (default: "summarize")
            max_words: Maximum number of words to include in filename
            
        Returns:
            A descriptive filename (without extension)
        """
        if not self.ai_processor_path or not text:
            return datetime.now().strftime("tts_%Y%m%d_%H%M%S")
            
        prompt = prompt_name or self.default_prompt
        words_limit = max_words or self.max_words
        
        try:
            # Create a temporary file with the text
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
                temp.write(text)
                temp_path = temp.name
                
            # Run the AI Text Processor
            cmd = [
                sys.executable,
                str(self.ai_processor_path),
                "--file", temp_path,
                "--prompt", prompt,
                "--max-tokens", "20"  # Keep it short
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            os.unlink(temp_path)  # Clean up temp file
            
            if result.returncode != 0:
                logging.warning(f"AI Text Processor failed: {result.stderr}")
                return datetime.now().strftime("tts_%Y%m%d_%H%M%S")
                
            # Process the output to create a filename
            summary = result.stdout.strip()
            
            # Keep only alphanumeric and spaces, convert to lowercase
            clean_summary = re.sub(r'[^a-zA-Z0-9\s]', '', summary).lower()
            
            # Split into words and take first max_words
            words = clean_summary.split()[:words_limit]
            
            # Join with underscores and add timestamp
            filename = "_".join(words) + "_" + datetime.now().strftime("%Y%m%d_%H%M%S")
            
            logging.info(f"Generated AI-based filename: {filename}")
            return filename
            
        except Exception as e:
            logging.error(f"Error generating AI filename: {str(e)}")
            return datetime.now().strftime("tts_%Y%m%d_%H%M%S")
    
    def determine_prompt(self, args) -> Optional[str]:
        """
        Determine which prompt to use based on command line arguments.
        
        Args:
            args: Command line arguments
            
        Returns:
            Prompt name to use, or None if AI filename generation is disabled
        """
        if hasattr(args, 'no_ai_filename') and args.no_ai_filename:
            return None
            
        # Get available prompts
        available_prompts = self.get_available_prompts()
        
        # Check if any specific prompt was requested
        for prompt in available_prompts:
            arg_name = f"ai_{prompt}"
            # Convert hyphens to underscores for argparse compatibility
            arg_name = arg_name.replace('-', '_')
            if hasattr(args, arg_name) and getattr(args, arg_name):
                return prompt
                
        # Default to summarize
        return self.default_prompt 