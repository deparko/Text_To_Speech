"""Google Text-to-Speech engine implementation."""

import os
import logging
from gtts import gTTS
import io
from . import config
from .base_engine import BaseTTSEngine

class GoogleTTSEngine(BaseTTSEngine):
    """Google TTS engine wrapper."""
    
    def __init__(self):
        """Initialize the Google TTS engine."""
        self.config = config.get_gtts_config()
        self.language = self.config.get('language', 'en')
        self.tld = self.config.get('tld', 'com')
        self.slow = self.config.get('slow', False)
        
    def generate_speech(self, text, **kwargs):
        """
        Generate speech from text using Google TTS.
        
        Args:
            text (str): The text to convert to speech
            **kwargs: Additional arguments (ignored for gTTS)
            
        Returns:
            bytes: The generated audio data in MP3 format
            
        Raises:
            Exception: If speech generation fails
        """
        try:
            logging.info(f"Generating speech using Google TTS (lang: {self.language})")
            
            # Create gTTS object
            tts = gTTS(
                text=text,
                lang=self.language,
                tld=self.tld,
                slow=self.slow
            )
            
            # Save to bytes buffer
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            return mp3_fp.getvalue()
            
        except Exception as e:
            logging.error(f"Error generating speech with Google TTS: {e}")
            raise
            
    @classmethod
    def get_name(cls):
        """Get the name of the TTS engine."""
        return "Google TTS"
        
    def get_format(self):
        """Get the audio format produced by this engine."""
        return "mp3"

def create_engine():
    """Factory function to create a Google TTS engine instance."""
    return GoogleTTSEngine() 