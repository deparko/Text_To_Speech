"""Test script for OpenAI TTS engine."""

import os
import sys
import logging
from pathlib import Path

# Add parent directory to path to import tts_core
sys.path.append(str(Path(__file__).parent.parent))
from tts_core import openai_tts

def test_voices():
    """Test listing available voices."""
    engine = openai_tts.create_engine()
    voices = engine.list_voices()
    print("\nAvailable voices:")
    for name, desc in voices.items():
        print(f"- {name}: {desc}")

def test_speech_generation():
    """Test speech generation with different voices."""
    engine = openai_tts.create_engine()
    
    # Test text (first paragraph of "A Farewell to Arms")
    text = """In the late summer of that year we lived in a house in a village that looked across the river and the plain to the mountains. In the bed of the river there were pebbles and boulders, dry and white in the sun, and the water was clear and swiftly moving and blue in the channels."""
    
    # Create output directory
    output_dir = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/TTS_Audio/openai_test"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test with different voices
    voices = ['nova', 'fable']  # Testing with two voices
    
    for voice in voices:
        print(f"\nGenerating speech with voice: {voice}")
        try:
            audio_data = engine.generate_speech(text, voice=voice)
            
            # Save the audio file
            output_file = output_dir / f"openai_test_{voice}.mp3"
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            print(f"Audio saved to: {output_file}")
            
            # Play the audio (macOS)
            os.system(f'afplay "{output_file}"')
            
        except Exception as e:
            print(f"Error testing voice {voice}: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Testing OpenAI TTS Engine")
    print("-" * 50)
    
    test_voices()
    test_speech_generation() 