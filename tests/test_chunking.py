"""
Test the text chunking functionality of the OpenAI TTS engine.
"""

import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tts_core.config import Config
from tts_core.openai_tts import OpenAITTSEngine

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def test_chunking():
    """Test text chunking with various edge cases."""
    
    # Create a minimal config
    config = Config()
    config.set('openai', 'api_key', os.getenv('OPENAI_API_KEY', 'dummy-key'))
    
    # Initialize the engine
    engine = OpenAITTSEngine(config)
    
    test_cases = [
        # Test case 1: Text with abbreviations
        {
            "name": "Abbreviations",
            "text": "Dr. Smith and Prof. Johnson went to Washington D.C. with Mr. and Mrs. Brown. They met Jr. executives from IBM Corp. and discussed A.I. technology.",
            "expected_chunks": 1
        },
        
        # Test case 2: Text with ellipsis
        {
            "name": "Ellipsis",
            "text": "He thought about it... and then decided to proceed. The path ahead seemed uncertain... but he knew what to do. Time passed... slowly at first... then all at once.",
            "expected_chunks": 1
        },
        
        # Test case 3: Text with quotes
        {
            "name": "Quoted text",
            "text": '''He said "This is a complete sentence inside quotes." Then he added "Another sentence that should stay together with more text to follow." Finally, he concluded.''',
            "expected_chunks": 1
        },
        
        # Test case 4: Very long sentence
        {
            "name": "Long sentence",
            "text": "This is an extremely long sentence that goes on and on, containing multiple clauses and phrases, separated by commas, semicolons, and other punctuation marks; it includes various ideas, concepts, and thoughts that are all connected together in a way that makes it difficult to find a natural breaking point, yet it needs to be split into smaller chunks because it exceeds the maximum character limit imposed by the API, which means we need to find appropriate places to break it up without disrupting the flow or meaning of the text, while still maintaining readability and coherence throughout the entire passage." * 10,
            "expected_chunks": 2
        },
        
        # Test case 5: Mixed case with everything
        {
            "name": "Mixed content",
            "text": '''Dr. Smith began his lecture: "The history of A.I. is fascinating..." He paused for effect. "From the early days of computing, through the A.I. winter, and into today's renaissance, we've seen tremendous progress." Prof. Johnson interjected, "But what about the ethical implications?" The discussion continued for hours, covering topics from machine learning to neural networks, from deep learning to natural language processing, and from computer vision to robotics. The students took careful notes as Dr. Smith explained: "The future of A.I. is both exciting and challenging..." ''' * 5,
            "expected_chunks": 1
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print("-" * 40)
        
        # Get chunks
        chunks = engine._split_text(test_case['text'])
        
        # Print results
        print(f"Number of chunks: {len(chunks)}")
        print(f"Expected chunks: {test_case['expected_chunks']}")
        
        for i, chunk in enumerate(chunks):
            print(f"\nChunk {i+1} ({len(chunk)} chars):")
            print("-" * 20)
            print(chunk[:100] + "..." if len(chunk) > 100 else chunk)
        
        # Verify each chunk is within limits
        for chunk in chunks:
            assert len(chunk) <= engine.MAX_CHARS, f"Chunk exceeds maximum length: {len(chunk)} chars"
        
        print("\nAll chunks within size limit ✓")

if __name__ == "__main__":
    test_chunking() 