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
        "use_gtts": False,  # Use as fallback
        "use_openai": True  # Default engine
    },
    "logging": {
        "verbose": False,
        "show_model_config": False
    },
    "gtts": {
        "language": "en",
        "tld": "com",
        "slow": False
    },
    "openai": {
        "voice": "nova",  # Default voice
        "model": "tts-1",
        "api_key": ""  # Set via OPENAI_API_KEY environment variable
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
        "add_to_music": False
    },
    "advanced": {
        "progress_bar": False,
        "gpu": False,
        "cost_tracking": True
    }
}

class Config:
    """Configuration manager for the TTS application."""
    
    def __init__(self, config_path=None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path (str or Path, optional): Path to the configuration file.
                If None, will look for tts_config.yaml in the script directory.
        """
        if config_path is None:
            script_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = script_dir / 'tts_config.yaml'
        elif isinstance(config_path, str):
            config_path = Path(config_path)
        
        self.config = DEFAULT_CONFIG.copy()
        self.config_path = config_path
        
        self.load_config(config_path)
    
    def load_config(self, config_path):
        """
        Load configuration from a YAML file.
        
        Args:
            config_path (Path): Path to the configuration file.
        
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
            config_path (str or Path, optional): Path to save the configuration file.
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

def load_config(config_path=None):
    """Helper function to create a Config instance."""
    return Config(config_path)

def get_config_path():
    """Get the path to the configuration file."""
    # Check current directory first
    local_config = Path("tts_config.yaml")
    if local_config.exists():
        return local_config
        
    # Check home directory
    home_config = Path.home() / ".tts_config.yaml"
    if home_config.exists():
        return home_config
        
    # Check deployment directory
    deploy_config = Path.home() / "SoftwareDev/bin/tts/tts_config.yaml"
    if deploy_config.exists():
        return deploy_config
        
    raise FileNotFoundError("Configuration file not found")

def load_config():
    """Load configuration from YAML file."""
    try:
        config_path = get_config_path()
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Expand user path in output folder
        if 'output' in config and 'folder' in config['output']:
            config['output']['folder'] = os.path.expanduser(config['output']['folder'])
            
        return config
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        raise

def get_engine_config():
    """Get the TTS engine configuration."""
    config = load_config()
    return {
        'use_gtts': config.get('model', {}).get('use_gtts', True),
        'use_openai': config.get('model', {}).get('use_openai', False),
        'model_name': config.get('model', {}).get('name'),
    }

def get_output_config():
    """Get the output configuration."""
    config = load_config()
    return config.get('output', {})

def get_voice_config():
    """Get the voice configuration."""
    config = load_config()
    return config.get('voice', {})

def get_openai_config():
    """Get OpenAI-specific configuration."""
    config = load_config()
    return config.get('openai', {})

def get_gtts_config():
    """Get Google TTS-specific configuration."""
    config = load_config()
    return config.get('gtts', {}) 