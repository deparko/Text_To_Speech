"""Test suite for TTS engines."""

import os
import sys
import unittest
from pathlib import Path
import logging

# Add parent directory to path to import tts_core
sys.path.append(str(Path(__file__).parent.parent))
from tts_core import config, openai_tts

class TestTTSEngines(unittest.TestCase):
    """Test cases for TTS engines."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.config = config.load_config()
        cls.test_text = "This is a test of the text-to-speech system."
        cls.test_dir = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/TTS_Audio/test"
        cls.test_dir.mkdir(parents=True, exist_ok=True)
    
    def test_gtts(self):
        """Test Google TTS engine."""
        from tts_core.gtts_engine import create_engine
        engine = create_engine()
        output_file = self.test_dir / "test_gtts.mp3"
        
        try:
            audio_data = engine.generate_speech(self.test_text)
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            self.assertTrue(output_file.exists())
            self.assertTrue(output_file.stat().st_size > 0)
        except Exception as e:
            self.fail(f"gTTS test failed: {e}")
    
    def test_coqui(self):
        """Test Coqui TTS engine."""
        try:
            from tts_core.coqui_engine import create_engine
            engine = create_engine()
            output_file = self.test_dir / "test_coqui.wav"
            
            audio_data = engine.generate_speech(self.test_text)
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            self.assertTrue(output_file.exists())
            self.assertTrue(output_file.stat().st_size > 0)
        except ImportError:
            logging.warning("Coqui TTS not installed, skipping test")
    
    def test_openai(self):
        """Test OpenAI TTS engine."""
        if not os.getenv('OPENAI_API_KEY'):
            logging.warning("OpenAI API key not set, skipping test")
            return
            
        engine = openai_tts.create_engine()
        
        # Test voice listing
        voices = engine.list_voices()
        self.assertIsInstance(voices, dict)
        self.assertGreater(len(voices), 0)
        
        # Test speech generation with different voices
        test_voices = ['nova', 'fable']
        for voice in test_voices:
            output_file = self.test_dir / f"test_openai_{voice}.mp3"
            try:
                audio_data = engine.generate_speech(self.test_text, voice=voice)
                with open(output_file, 'wb') as f:
                    f.write(audio_data)
                self.assertTrue(output_file.exists())
                self.assertTrue(output_file.stat().st_size > 0)
            except Exception as e:
                self.fail(f"OpenAI TTS test failed for voice {voice}: {e}")

def run_tests():
    """Run the test suite."""
    logging.basicConfig(level=logging.INFO)
    unittest.main(argv=[''], verbosity=2)

if __name__ == '__main__':
    run_tests() 