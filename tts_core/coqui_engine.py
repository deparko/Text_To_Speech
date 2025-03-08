"""Coqui TTS engine implementation."""

import os
import logging
import io
import wave
import numpy as np
from . import config
from .base_engine import BaseTTSEngine

class CoquiTTSEngine(BaseTTSEngine):
    """Coqui TTS engine wrapper."""
    
    def __init__(self):
        """Initialize the Coqui TTS engine."""
        try:
            from TTS.api import TTS
            self.config = config.load_config()
            model_name = self.config.get('model', {}).get('name')
            self.tts = TTS(model_name=model_name, progress_bar=False)
            logging.info(f"Initialized Coqui TTS with model: {model_name}")
        except ImportError as e:
            logging.error(f"Error loading Coqui TTS: {e}")
            raise
            
    def generate_speech(self, text, **kwargs):
        """
        Generate speech from text using Coqui TTS.
        
        Args:
            text (str): The text to convert to speech
            **kwargs: Additional parameters:
                - speed (float): Speech speed multiplier
                - speaker_id (int): Speaker ID for multi-speaker models
            
        Returns:
            bytes: The generated audio data in WAV format
            
        Raises:
            Exception: If speech generation fails
        """
        try:
            # Get voice parameters
            speed = kwargs.get('speed', self.config.get('voice', {}).get('speed', 1.0))
            speaker_id = kwargs.get('speaker_id', self.config.get('voice', {}).get('speaker_id'))
            
            # Generate audio
            wav = self.tts.tts(
                text=text,
                speaker_id=speaker_id,
                speed=speed
            )
            
            # Convert to bytes
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wavfile:
                wavfile.setnchannels(1)  # mono
                wavfile.setsampwidth(2)  # 16-bit
                wavfile.setframerate(self.config.get('voice', {}).get('sample_rate', 22050))
                wavfile.writeframes(np.array(wav).tobytes())
            
            return wav_buffer.getvalue()
            
        except Exception as e:
            logging.error(f"Error generating speech with Coqui TTS: {e}")
            raise
            
    @classmethod
    def get_name(cls):
        """Get the name of the TTS engine."""
        return "Coqui TTS"
        
    def get_format(self):
        """Get the audio format produced by this engine."""
        return "wav"
        
    def list_models(self):
        """List available TTS models."""
        try:
            from TTS.api import TTS
            models = TTS().list_models()
            return [m for m in models if "tts_models" in m]
        except ImportError:
            return []

def create_engine():
    """Factory function to create a Coqui TTS engine instance."""
    return CoquiTTSEngine() 