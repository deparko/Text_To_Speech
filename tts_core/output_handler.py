"""
Output handling for the Text-to-Speech application.
This module handles audio file output and playback.
"""

import os
import logging
import hashlib
import subprocess
from datetime import datetime

class OutputHandler:
    """Handles audio output and file management."""
    
    def __init__(self, config):
        """Initialize the output handler with configuration."""
        self.config = config
        
        # Set up output directory (iCloud Drive)
        self.output_dir = os.path.expanduser(config.get("output", "folder"))
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set up cache if enabled
        self.use_cache = config.get("output", "cache_audio", False)
        if self.use_cache:
            self.cache_dir = os.path.join(self.output_dir, "cache")
            os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_log_path(self):
        """Get the path for the log file."""
        log_dir = os.path.join(self.output_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(log_dir, f"tts_{timestamp}.log")
    
    def save_audio(self, audio_data, format_ext):
        """
        Save audio data to a file.
        
        Args:
            audio_data (bytes): The audio data to save
            format_ext (str): The file format extension (e.g., 'mp3', 'wav')
            
        Returns:
            str: Path to the saved audio file
        """
        # Check cache first if enabled
        if self.use_cache:
            cache_key = hashlib.md5(audio_data).hexdigest()
            cache_path = os.path.join(self.cache_dir, f"cache_{cache_key}.{format_ext}")
            
            if os.path.exists(cache_path):
                logging.info(f"Using cached audio: {cache_path}")
                return self._process_audio_file(cache_path, format_ext)
            
        # Generate new file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"tts_{timestamp}.{format_ext}")
        
        with open(output_path, 'wb') as f:
            f.write(audio_data)
        
        # Cache if enabled
        if self.use_cache:
            with open(cache_path, 'wb') as f:
                f.write(audio_data)
            logging.info(f"Audio cached for future use: {cache_path}")
        
        return self._process_audio_file(output_path, format_ext)
    
    def _process_audio_file(self, file_path, format_ext):
        """
        Process the audio file.
        
        Args:
            file_path (str): Path to the audio file
            format_ext (str): The file format extension
            
        Returns:
            str: Path to the processed audio file
        """
        # Only try to add to Music if explicitly enabled
        if self.config.get("output", "add_to_music", False):
            try:
                cmd = ['osascript', '-e', f'tell application "Music" to add POSIX file "{file_path}"']
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    logging.info(f"Added to Music library: {file_path} ({result.stdout.strip()})")
                else:
                    logging.error(f"Error adding to Music library: {result.stderr}")
            except Exception as e:
                logging.error(f"Error adding to Music library: {e}")
        
        return file_path
    
    def play_audio(self, file_path):
        """
        Play an audio file.
        
        Args:
            file_path (str): Path to the audio file to play
        """
        if not self.config.get("output", "play_audio", True):
            return
            
        try:
            cmd = ['afplay', file_path]
            subprocess.run(cmd, check=True)
            logging.info(f"Played audio file: {file_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error playing audio: {e}")
        except Exception as e:
            logging.error(f"Error playing audio: {e}") 