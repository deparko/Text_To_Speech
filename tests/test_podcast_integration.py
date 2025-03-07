"""
Test suite for podcast integration functionality.
"""

import os
import unittest
import tempfile
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime
import yaml

from tts_core.config import Config
from tts_core.podcast_handler import PodcastHandler

class TestPodcastIntegration(unittest.TestCase):
    """Test cases for podcast integration."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.podcast_dir = os.path.join(self.test_dir, "podcast")
        self.audio_dir = os.path.join(self.test_dir, "audio")
        
        # Create test config file
        self.config_data = {
            "model": {
                "name": "tts_models/en/ljspeech/tacotron2-DDC",
                "use_gtts": True
            },
            "voice": {
                "speed": 1.0,
                "speaker_id": None,
                "pitch": None
            },
            "output": {
                "folder": self.audio_dir,
                "play_audio": False,
                "cache_audio": False
            },
            "podcast": {
                "enabled": True,
                "folder": self.podcast_dir,
                "title": "Test Podcast",
                "description": "Test Description",
                "author": "Test Author",
                "add_to_itunes": False  # Disable iTunes integration for tests
            }
        }
        
        # Write config to file
        self.config_file = os.path.join(self.test_dir, "test_config.yaml")
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config_data, f)
        
        # Create test audio file
        os.makedirs(self.audio_dir)
        self.test_audio = os.path.join(self.audio_dir, "test.mp3")
        with open(self.test_audio, "wb") as f:
            f.write(b"dummy audio data")
    
    def tearDown(self):
        """Clean up after each test."""
        shutil.rmtree(self.test_dir)
    
    def test_podcast_initialization(self):
        """Test podcast handler initialization."""
        handler = PodcastHandler(Config(self.config_file))
        
        # Check if podcast directory was created
        self.assertTrue(os.path.exists(self.podcast_dir))
        
        # Check if feed file was created
        feed_file = os.path.join(self.podcast_dir, "feed.xml")
        self.assertTrue(os.path.exists(feed_file))
        
        # Verify feed content
        tree = ET.parse(feed_file)
        root = tree.getroot()
        channel = root.find("channel")
        
        self.assertEqual(channel.find("title").text, "Test Podcast")
        self.assertEqual(channel.find("description").text, "Test Description")
        self.assertEqual(channel.find("author").text, "Test Author")
    
    def test_add_episode(self):
        """Test adding an episode to the podcast."""
        handler = PodcastHandler(Config(self.config_file))
        
        # Add test episode
        title = "Test Episode"
        success = handler.add_episode(self.test_audio, title)
        
        self.assertTrue(success)
        
        # Verify episode in feed
        tree = ET.parse(os.path.join(self.podcast_dir, "feed.xml"))
        root = tree.getroot()
        items = root.findall(".//item")
        
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].find("title").text, title)
        
        # Verify audio file was copied
        episode_files = [f for f in os.listdir(self.podcast_dir) if f.endswith(".mp3")]
        self.assertEqual(len(episode_files), 1)
    
    def test_duplicate_episode(self):
        """Test adding the same episode twice."""
        handler = PodcastHandler(Config(self.config_file))
        
        # Add same episode twice
        handler.add_episode(self.test_audio, "First Try")
        handler.add_episode(self.test_audio, "Second Try")
        
        # Verify two separate episodes were created
        episode_files = [f for f in os.listdir(self.podcast_dir) if f.endswith(".mp3")]
        self.assertEqual(len(episode_files), 2)
    
    def test_invalid_audio_file(self):
        """Test handling of invalid audio file."""
        handler = PodcastHandler(Config(self.config_file))
        
        # Try to add non-existent file
        success = handler.add_episode("nonexistent.mp3", "Should Fail")
        
        self.assertFalse(success)
        
        # Verify no episode was added
        episode_files = [f for f in os.listdir(self.podcast_dir) if f.endswith(".mp3")]
        self.assertEqual(len(episode_files), 0)
    
    def test_feed_update(self):
        """Test that feed is properly updated."""
        handler = PodcastHandler(Config(self.config_file))
        
        # Add multiple episodes
        episodes = [
            ("Episode 1", "test1.mp3"),
            ("Episode 2", "test2.mp3"),
            ("Episode 3", "test3.mp3")
        ]
        
        for title, filename in episodes:
            test_audio = os.path.join(self.audio_dir, filename)
            with open(test_audio, "wb") as f:
                f.write(b"dummy audio data")
            handler.add_episode(test_audio, title)
        
        # Verify feed content
        tree = ET.parse(os.path.join(self.podcast_dir, "feed.xml"))
        root = tree.getroot()
        items = root.findall(".//item")
        
        self.assertEqual(len(items), 3)
        for i, item in enumerate(items):
            self.assertEqual(item.find("title").text, f"Episode {3-i}")

if __name__ == "__main__":
    unittest.main() 