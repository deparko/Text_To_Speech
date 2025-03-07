"""
Configuration handling for the Text-to-Speech application.
"""

import os
import yaml
from pathlib import Path
import logging

# Default configuration
DEFAULT_CONFIG = {
    "model": {
        "name": "tts_models/en/ljspeech/tacotron2-DDC",
        "alternatives": [
            "tts_models/en/ljspeech/fast_pitch",
            "tts_models/en/vctk/fast_pitch",
            "tts_models/en/vctk/vits"
        ],
        "use_gtts": True
    },
    "gtts": {
        "language": "en",
        "tld": "com",
        "slow": False
    },
    "voice": {
        "speed": 1.0,
        "speaker_id": None,
        "pitch": None,
        "sample_rate": 22050
    },
    "output": {
        "folder": "~/Library/Mobile Documents/com~apple~CloudDocs/TTS_Audio",
        "play_audio": True,
        "cache_audio": False,
        "add_to_music": True
    },
    "ai": {
        "api_key": "",
        "model": "gpt-3.5-turbo",
        "temperature": 0.3,
        "max_tokens": 1000,
        "target_language": "English"
    },
    "advanced": {
        "progress_bar": False,
        "gpu": False,
        "stream": False
    }
}

class Config:
    """Configuration manager for the TTS application."""
    
    def __init__(self, config_path=None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path (str, optional): Path to the configuration file.
                If None, will look for tts_config.yaml in the current directory.
        """
        self.config = DEFAULT_CONFIG.copy()
        self.config_path = config_path
        
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path):
        """
        Load configuration from a YAML file.
        
        Args:
            config_path (str): Path to the configuration file.
        
        Returns:
            dict: The loaded configuration.
        """
        try:
            with open(config_path, 'r') as file:
                yaml_config = yaml.safe_load(file)
                
                # Update default config with values from file
                if yaml_config:
                    # Merge dictionaries
                    for section in yaml_config:
                        if section in self.config:
                            self.config[section].update(yaml_config[section])
                        else:
                            self.config[section] = yaml_config[section]
                            
                # Expand user directory in output folder path
                self.config["output"]["folder"] = os.path.expanduser(self.config["output"]["folder"])
                
                logging.info(f"Configuration loaded from {config_path}")
                
        except FileNotFoundError:
            logging.warning(f"Config file {config_path} not found. Using defaults.")
        except yaml.YAMLError as e:
            logging.error(f"Error parsing config file: {e}. Using defaults.")
        
        return self.config
    
    def get(self, section, key=None, default=None):
        """
        Get a configuration value.
        
        Args:
            section (str): The configuration section.
            key (str, optional): The configuration key within the section.
                If None, returns the entire section.
            default: The default value to return if the key is not found.
        
        Returns:
            The configuration value, or default if not found.
        """
        if section not in self.config:
            return default
            
        if key is None:
            return self.config[section]
            
        return self.config[section].get(key, default)
    
    def set(self, section, key, value):
        """
        Set a configuration value.
        
        Args:
            section (str): The configuration section.
            key (str): The configuration key within the section.
            value: The value to set.
        """
        if section not in self.config:
            self.config[section] = {}
            
        self.config[section][key] = value
    
    def save(self, config_path=None):
        """
        Save the configuration to a YAML file.
        
        Args:
            config_path (str, optional): Path to save the configuration file.
                If None, uses the path from initialization.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        path = config_path or self.config_path
        if not path:
            logging.error("No configuration path specified for saving.")
            return False
            
        try:
            with open(path, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False)
            logging.info(f"Configuration saved to {path}")
            return True
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")
            return False 