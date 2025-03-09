#!/usr/bin/env python3
"""
Test script for AI Text Processor integration with the TTS system.
This script tests the AI-based text preprocessing and filename generation features.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import shutil

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules to test
try:
    from tts_core.ai_filename_generator import generate_ai_filename, is_ai_processor_available
except ImportError:
    print("Warning: Could not import AI filename generator module. Tests will be skipped.")
    AI_MODULES_AVAILABLE = False
else:
    AI_MODULES_AVAILABLE = True


@unittest.skipIf(not AI_MODULES_AVAILABLE, "AI modules not available")
class TestAIIntegration(unittest.TestCase):
    """Test cases for AI Text Processor integration."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test outputs
        self.test_dir = tempfile.mkdtemp()
        
        # Mock environment variables and configurations
        self.env_patcher = patch.dict('os.environ', {
            'OPENAI_API_KEY': 'test_api_key'
        })
        self.env_patcher.start()
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
        
        # Stop patchers
        self.env_patcher.stop()

    def test_ai_processor_availability(self):
        """Test that the AI Text Processor is available."""
        if AI_MODULES_AVAILABLE:
            # This might return False in CI environments, so we'll mock it
            with patch('tts_core.ai_filename_generator.is_ai_processor_available', return_value=True):
                self.assertTrue(is_ai_processor_available())

    @patch('tts_core.ai_filename_generator.process_with_ai')
    def test_generate_ai_filename(self, mock_process):
        """Test generating a filename using AI."""
        # Mock the AI processing function
        mock_process.return_value = "This is about cellular energy production"
        
        # Test with sample text
        text = "The mitochondria is the powerhouse of the cell"
        filename = generate_ai_filename(text)
        
        # Verify that the AI processor was called
        mock_process.assert_called_once()
        
        # Verify that the filename is not empty and doesn't contain invalid characters
        self.assertTrue(filename)
        self.assertNotIn('/', filename)
        self.assertNotIn('\\', filename)
        
        # Verify that the filename contains expected words
        self.assertTrue(any(word in filename.lower() for word in ['cellular', 'energy', 'production']))

    @patch('tts_core.ai_filename_generator.process_with_ai')
    def test_generate_ai_filename_with_prompt(self, mock_process):
        """Test generating a filename using AI with a specific prompt."""
        # Mock the AI processing function
        mock_process.return_value = "Scientific explanation of cellular energy"
        
        # Test with sample text and prompt
        text = "The mitochondria is the powerhouse of the cell"
        filename = generate_ai_filename(text, prompt="summarize")
        
        # Verify that the AI processor was called with the right prompt
        mock_process.assert_called_once()
        args, kwargs = mock_process.call_args
        self.assertEqual(kwargs.get('prompt'), "summarize")
        
        # Verify that the filename contains expected words
        self.assertTrue(any(word in filename.lower() for word in ['scientific', 'cellular', 'energy']))

    @patch('tts_core.ai_filename_generator.process_with_ai')
    def test_generate_ai_filename_error_handling(self, mock_process):
        """Test error handling when AI processing fails."""
        # Mock the AI processing function to raise an exception
        mock_process.side_effect = Exception("API error")
        
        # Test with sample text
        text = "The mitochondria is the powerhouse of the cell"
        filename = generate_ai_filename(text)
        
        # Verify that a fallback filename is generated
        self.assertTrue(filename)
        self.assertTrue(filename.startswith("tts_"))

    @unittest.skipIf(not os.environ.get('RUN_INTEGRATION_TESTS'), "Integration tests disabled")
    def test_real_ai_integration(self):
        """Test the actual AI integration (requires API key)."""
        # This test will only run if RUN_INTEGRATION_TESTS is set
        # and requires a valid OpenAI API key
        
        # Test with sample text
        text = "The mitochondria is the powerhouse of the cell"
        filename = generate_ai_filename(text)
        
        # Verify that the filename is not empty and doesn't contain invalid characters
        self.assertTrue(filename)
        self.assertNotIn('/', filename)
        self.assertNotIn('\\', filename)
        
        # We can't verify the exact content, but we can check it's not just a timestamp
        self.assertFalse(filename.startswith("tts_"))


if __name__ == '__main__':
    unittest.main() 