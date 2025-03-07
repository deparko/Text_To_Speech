"""
TTS engine interface for the Text-to-Speech application.
Provides a unified interface for different TTS engines.
"""

import os
import logging
from gtts import gTTS

class TTSEngine:
    """Interface for TTS engines."""
    
    def __init__(self, config):
        """Initialize the TTS engine with configuration."""
        self.config = config
        self.use_gtts = config.get("model", "use_gtts", False)
        
        if not self.use_gtts:
            try:
                import torch
                from TTS.api import TTS
                
                model_name = config.get("model", "name")
                self.tts = TTS(model_name=model_name, progress_bar=False)
                logging.info(f"Initialized Coqui TTS with model: {model_name}")
            except ImportError as e:
                logging.error(f"Error loading Coqui TTS: {e}")
                logging.info("Falling back to Google TTS")
                self.use_gtts = True
    
    def generate_speech(self, text):
        """
        Generate speech from text.
        
        Args:
            text (str): Text to convert to speech
            
        Returns:
            bytes: Audio data in WAV or MP3 format
        """
        if self.use_gtts:
            return self._generate_gtts(text)
        else:
            return self._generate_coqui(text)
    
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
    
    def _generate_coqui(self, text):
        """Generate speech using Coqui TTS."""
        try:
            # Get voice parameters
            speed = self.config.get("voice", "speed", 1.0)
            speaker_id = self.config.get("voice", "speaker_id", None)
            
            # Generate audio
            wav = self.tts.tts(
                text=text,
                speaker_id=speaker_id,
                speed=speed
            )
            
            # Convert to bytes
            import io
            import wave
            import numpy as np
            
            # Create WAV file in memory
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wavfile:
                wavfile.setnchannels(1)  # mono
                wavfile.setsampwidth(2)  # 16-bit
                wavfile.setframerate(self.config.get("voice", "sample_rate", 22050))
                wavfile.writeframes(np.array(wav).tobytes())
            
            return wav_buffer.getvalue()
            
        except Exception as e:
            logging.error(f"Error generating speech with Coqui TTS: {e}")
            return None
    
    def list_voices(self):
        """List available voices/models."""
        if self.use_gtts:
            print("Using Google TTS - no additional voices available")
            return
        
        try:
            from TTS.api import TTS
            models = TTS().list_models()
            print("\nAvailable TTS models:")
            for model in models:
                if "tts_models" in model:
                    print(f"- {model}")
        except ImportError as e:
            logging.error(f"Error listing voices: {e}")
            print("Could not list voices - TTS package not available") 