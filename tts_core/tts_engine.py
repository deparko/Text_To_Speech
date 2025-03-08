"""
TTS engine interface for the Text-to-Speech application.
Provides a unified interface for different TTS engines.
"""

import os
import logging
from gtts import gTTS
from .openai_tts import OpenAITTSEngine

class TTSEngine:
    """Interface for TTS engines."""
    
    def __init__(self, config):
        """Initialize the TTS engine with configuration."""
        self.config = config
        self.use_gtts = config.get("model", "use_gtts", False)
        self.use_openai = config.get("model", "use_openai", True)
        self.engine = None
        
        if self.use_openai:
            try:
                self.engine = OpenAITTSEngine(config)
                logging.info("Using OpenAI TTS engine")
            except Exception as e:
                logging.error(f"Error initializing OpenAI TTS: {e}")
                logging.info("Falling back to Google TTS")
                self.use_gtts = True
                self.use_openai = False
        
        if self.use_gtts:
            logging.info("Using Google TTS engine")
    
    def generate_speech(self, text):
        """
        Generate speech from text.
        
        Args:
            text (str): Text to convert to speech
            
        Returns:
            bytes: Audio data in WAV or MP3 format
        """
        if self.use_openai:
            return self._generate_openai(text)
        elif self.use_gtts:
            return self._generate_gtts(text)
        else:
            logging.error("No TTS engine available")
            return None
    
    def _generate_openai(self, text):
        """Generate speech using OpenAI TTS."""
        try:
            return self.engine.generate_speech(text)
        except Exception as e:
            logging.error(f"Error generating speech with OpenAI TTS: {e}")
            if not self.use_gtts:
                logging.info("Falling back to Google TTS")
                self.use_gtts = True
                return self._generate_gtts(text)
            return None
    
    def _generate_gtts(self, text):
        """Generate speech using Google TTS."""
        try:
            tts = gTTS(
                text=text,
                lang=self.config.get("gtts", "language", "en"),
                tld=self.config.get("gtts", "tld", "com"),
                slow=self.config.get("gtts", "slow", False)
            )
            
            # Save to bytes buffer
            import io
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            return mp3_fp.getvalue()
            
        except Exception as e:
            logging.error(f"Error generating speech with Google TTS: {e}")
            return None
    
    def list_voices(self):
        """List available voices/models."""
        if self.use_openai and self.engine:
            self.engine.list_voices()
        elif self.use_gtts:
            print("\nUsing Google TTS - no additional voices available") 