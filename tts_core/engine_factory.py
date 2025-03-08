"""TTS engine factory and coordinator."""

import logging
from . import config
from . import gtts_engine
from . import openai_tts
from . import coqui_engine

class TTSEngineFactory:
    """Factory class for creating and managing TTS engines."""
    
    def __init__(self):
        """Initialize the TTS engine factory."""
        self.config = config.load_config()
        self._engines = {}
        
    def get_engine(self, engine_type=None):
        """
        Get a TTS engine instance.
        
        Args:
            engine_type (str, optional): Type of engine to use:
                - 'gtts': Google TTS
                - 'coqui': Coqui TTS
                - 'openai': OpenAI TTS
                If None, uses configuration to determine engine
        
        Returns:
            BaseTTSEngine: The TTS engine instance
            
        Raises:
            ValueError: If engine type is invalid or engine creation fails
        """
        # Determine engine type from config if not specified
        if engine_type is None:
            if self.config.get('model', {}).get('use_openai', False):
                engine_type = 'openai'
            elif self.config.get('model', {}).get('use_gtts', True):
                engine_type = 'gtts'
            else:
                engine_type = 'coqui'
        
        # Return cached engine if available
        if engine_type in self._engines:
            return self._engines[engine_type]
        
        # Create new engine instance
        try:
            if engine_type == 'gtts':
                engine = gtts_engine.create_engine()
            elif engine_type == 'coqui':
                engine = coqui_engine.create_engine()
            elif engine_type == 'openai':
                engine = openai_tts.create_engine()
            else:
                raise ValueError(f"Invalid engine type: {engine_type}")
                
            self._engines[engine_type] = engine
            logging.info(f"Created {engine.get_name()} engine")
            return engine
            
        except Exception as e:
            logging.error(f"Error creating {engine_type} engine: {e}")
            
            # Fall back to Google TTS if other engines fail
            if engine_type != 'gtts':
                logging.info("Falling back to Google TTS")
                return self.get_engine('gtts')
            else:
                raise
    
    def list_available_engines(self):
        """List all available TTS engines."""
        engines = []
        
        # Try Google TTS
        try:
            engine = self.get_engine('gtts')
            engines.append({
                'name': engine.get_name(),
                'type': 'gtts',
                'format': engine.get_format()
            })
        except Exception:
            pass
            
        # Try Coqui TTS
        try:
            engine = self.get_engine('coqui')
            engines.append({
                'name': engine.get_name(),
                'type': 'coqui',
                'format': engine.get_format()
            })
        except Exception:
            pass
            
        # Try OpenAI TTS
        try:
            engine = self.get_engine('openai')
            engines.append({
                'name': engine.get_name(),
                'type': 'openai',
                'format': engine.get_format(),
                'voices': engine.list_voices()
            })
        except Exception:
            pass
            
        return engines

def create_factory():
    """Create a new TTS engine factory instance."""
    return TTSEngineFactory() 