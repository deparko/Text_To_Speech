"""Base interface for TTS engines."""

from abc import ABC, abstractmethod

class BaseTTSEngine(ABC):
    """Abstract base class for TTS engines."""
    
    @abstractmethod
    def generate_speech(self, text, **kwargs):
        """
        Generate speech from text.
        
        Args:
            text (str): The text to convert to speech
            **kwargs: Additional engine-specific parameters
            
        Returns:
            bytes: The generated audio data
            
        Raises:
            Exception: If speech generation fails
        """
        pass
    
    @classmethod
    def get_name(cls):
        """Get the name of the TTS engine."""
        return cls.__name__
        
    def get_format(self):
        """Get the audio format produced by this engine."""
        return "mp3"  # Default format, override if different 