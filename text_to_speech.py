import pyperclip
import os
import platform
import argparse
import yaml
import hashlib
from datetime import datetime

# Add gTTS import
try:
    from gtts import gTTS
except ImportError:
    gTTS = None

# Parse command line arguments first to check for --use-gtts
parser = argparse.ArgumentParser(description='Convert clipboard text to speech')
parser.add_argument('--speed', type=float, help='Speech speed multiplier')
parser.add_argument('--model', type=str, help='TTS model to use')
parser.add_argument('--no-play', action='store_true', help='Do not play audio after generation')
parser.add_argument('--speaker', type=int, help='Speaker ID for multi-speaker models')
parser.add_argument('--pitch', type=float, help='Voice pitch adjustment')
parser.add_argument('--config', type=str, default='tts_config.yaml', help='Path to config file')
parser.add_argument('--list-voices', action='store_true', help='List available TTS models and exit')
parser.add_argument('--use-gtts', action='store_true', help='Use Google TTS instead of local models')

args, _ = parser.parse_known_args()

# Load configuration
def load_config(config_path="tts_config.yaml"):
    """Load configuration from YAML file."""
    # Default configuration
    default_config = {
        "model": {
            "name": "tts_models/en/ljspeech/tacotron2-DDC",
            "alternatives": [],
            "use_gtts": False
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
            "folder": "~/Documents/TTS_Audio",
            "play_audio": True,
            "cache_audio": True
        },
        "advanced": {
            "progress_bar": False,
            "gpu": False
        }
    }
    
    # Try to load from file
    config = default_config
    try:
        with open(config_path, 'r') as file:
            yaml_config = yaml.safe_load(file)
            # Update default config with values from file
            if yaml_config:
                # Merge dictionaries (this is a simple approach)
                if "model" in yaml_config:
                    config["model"].update(yaml_config["model"])
                if "gtts" in yaml_config:
                    config["gtts"].update(yaml_config["gtts"])
                if "voice" in yaml_config:
                    config["voice"].update(yaml_config["voice"])
                if "output" in yaml_config:
                    config["output"].update(yaml_config["output"])
                if "advanced" in yaml_config:
                    config["advanced"].update(yaml_config["advanced"])
    except FileNotFoundError:
        print(f"Config file {config_path} not found. Using defaults.")
    except yaml.YAMLError as e:
        print(f"Error parsing config file: {e}. Using defaults.")
    
    # Expand user directory in output folder path
    config["output"]["folder"] = os.path.expanduser(config["output"]["folder"])
    
    return config

# Load configuration
config = load_config(args.config if args.config else "tts_config.yaml")

# Determine if we should use Google TTS
USE_GTTS = args.use_gtts if args.use_gtts is not None else config["model"]["use_gtts"]

# Only import TTS if we're not using Google TTS
if not USE_GTTS:
    try:
        from TTS.api import TTS
    except ImportError:
        print("Error: TTS module not found. If you want to use local TTS models, please install it with:")
        print("pip install TTS")
        print("Alternatively, use Google TTS with --use-gtts option")
        exit(1)

# Extract configuration values
GTTS_LANG = config["gtts"]["language"]
GTTS_TLD = config["gtts"]["tld"]
GTTS_SLOW = config["gtts"]["slow"]
MODEL_NAME = config["model"]["name"]
SPEECH_SPEED = config["voice"]["speed"]
SPEAKER_ID = config["voice"]["speaker_id"]
PITCH = config["voice"]["pitch"]
SAMPLE_RATE = config["voice"]["sample_rate"]
OUTPUT_FOLDER = config["output"]["folder"]
PLAY_AUDIO = config["output"]["play_audio"]
CACHE_AUDIO = config["output"]["cache_audio"]
PROGRESS_BAR = config["advanced"]["progress_bar"]
USE_GPU = config["advanced"]["gpu"]

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize TTS with configuration (only if not using gTTS)
if not USE_GTTS:
    tts = TTS(MODEL_NAME, progress_bar=PROGRESS_BAR, gpu=USE_GPU)
else:
    # Check if gTTS is installed
    if gTTS is None:
        print("Google TTS is enabled in config but the 'gtts' package is not installed.")
        print("Installing it now with: pip install gtts")
        import subprocess
        subprocess.check_call(["pip", "install", "gtts"])
        from gtts import gTTS
    print("Using Google Text-to-Speech")

def play_audio(file_path):
    """Play audio file based on the operating system."""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        # macOS can play both MP3 and WAV with afplay
        os.system(f"afplay \"{file_path}\"")
    elif system == "Windows":
        # Windows can play both with the start command
        os.system(f"start \"{file_path}\"")
    elif system == "Linux":
        # For Linux, try to detect the file type and use appropriate player
        if file_path.endswith(".mp3"):
            # Try mpg123 first, fall back to generic player
            if os.system(f"which mpg123 > /dev/null") == 0:
                os.system(f"mpg123 \"{file_path}\"")
            else:
                os.system(f"xdg-open \"{file_path}\"")
        else:
            # WAV files
            os.system(f"aplay \"{file_path}\"")
    else:
        print(f"Unsupported OS: {system}. Please play the file manually: {file_path}")

def speak_clipboard(speed=None, model=None, play=None, speaker_id=None, pitch=None, use_gtts=None):
    """Reads text from the clipboard, converts it to speech, saves the file, and plays it."""
    text = pyperclip.paste().strip()
    
    if not text:
        print("Clipboard is empty!")
        return

    # Use provided parameters or defaults from config
    speech_speed = speed if speed is not None else SPEECH_SPEED
    tts_model = model if model is not None else MODEL_NAME
    should_play = play if play is not None else PLAY_AUDIO
    speaker = speaker_id if speaker_id is not None else SPEAKER_ID
    voice_pitch = pitch if pitch is not None else PITCH
    use_google_tts = use_gtts if use_gtts is not None else USE_GTTS
    
    # Determine file extension based on TTS engine
    file_ext = "mp3" if use_google_tts else "wav"
    
    # Check if we should use cached audio
    if CACHE_AUDIO:
        # Create hash of text and parameters for caching
        cache_key = f"{text}_{speech_speed}_{tts_model}_{speaker}_{voice_pitch}_{use_google_tts}"
        text_hash = hashlib.md5(cache_key.encode()).hexdigest()
        cache_path = os.path.join(OUTPUT_FOLDER, f"cache_{text_hash}.{file_ext}")
        
        # Use cached file if it exists
        if os.path.exists(cache_path):
            print("Using cached audio")
            if should_play:
                play_audio(cache_path)
            return cache_path

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"tts_{timestamp}.{file_ext}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    print(f"Generating speech file: {output_filename}")
    
    # Use Google TTS or local TTS based on configuration
    if use_google_tts:
        # Generate speech with Google TTS (directly to MP3)
        gtts = gTTS(text=text, lang=GTTS_LANG, tld=GTTS_TLD, slow=GTTS_SLOW)
        gtts.save(output_path)
        
        # Note: We're not attempting to convert to WAV or adjust speed
        # since you're fine with MP3 files
        print(f"Generated MP3 file with Google TTS")
    else:
        # Use local TTS (outputs WAV)
        # Prepare TTS parameters
        tts_kwargs = {"text": text, "file_path": output_path, "speed": speech_speed}
        
        # Add optional parameters if they're set AND compatible with the model
        # Only add speaker parameter for multi-speaker models
        if speaker is not None and ("vctk" in tts_model or "multi" in tts_model):
            tts_kwargs["speaker"] = speaker
        elif speaker is not None:
            print("Warning: Speaker ID provided but current model doesn't support multiple speakers.")
            print("Speaker ID will be ignored.")
        
        # Add pitch if set
        if voice_pitch is not None:
            tts_kwargs["pitch"] = voice_pitch
        
        # Convert text to speech and save it
        tts.tts_to_file(**tts_kwargs)

    print(f"Audio saved to: {output_path}")
    
    # If caching is enabled, save a copy in the cache
    if CACHE_AUDIO:
        import shutil
        shutil.copy2(output_path, cache_path)
        print(f"Audio cached for future use")
    
    # Play the generated audio if requested
    if should_play:
        play_audio(output_path)
        
    return output_path

def list_available_voices():
    """List all available TTS models and speakers."""
    print("Available TTS models:")
    # Create a temporary TTS instance to list models
    temp_tts = TTS()
    
    # Get the model list - the API has changed
    model_manager = temp_tts.list_models()
    
    # List TTS models
    print("\nText-to-Speech models:")
    for model_type in model_manager.list_tts_models():
        print(f"- {model_type}")
    
    # List vocoder models if needed
    print("\nVocoder models:")
    for vocoder in model_manager.list_vocoder_models():
        print(f"- {vocoder}")
        
    # If using a multi-speaker model, list available speakers
    if "vctk" in MODEL_NAME or "multi" in MODEL_NAME:
        print("\nThis model supports multiple speakers.")
        print("You can set speaker_id in the config file or via command line.")

# Run the function
if __name__ == "__main__":
    # List available voices if requested
    if args.list_voices:
        list_available_voices()
        exit(0)
    
    speak_clipboard(
        speed=args.speed,
        model=args.model,
        play=not args.no_play if args.no_play else None,
        speaker_id=args.speaker,
        pitch=args.pitch,
        use_gtts=args.use_gtts if args.use_gtts else None
    )