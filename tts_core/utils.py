"""
Utility functions for the Text-to-Speech application.
"""

import os
import sys
import logging
import platform
import subprocess
from datetime import datetime

def setup_logging(log_dir=None, level=logging.INFO):
    """
    Set up logging for the application.
    
    Args:
        log_dir (str, optional): Directory to store log files.
            If None, logs will be stored in ~/Documents/TTS_Audio/logs.
        level: Logging level (default: INFO).
    """
    if log_dir is None:
        log_dir = os.path.expanduser("~/Documents/TTS_Audio/logs")
        
    os.makedirs(log_dir, exist_ok=True)
    
    # Create a timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"tts_{timestamp}.log")
    
    # Configure logging
    logging.basicConfig(
        filename=log_file,
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Also log to console
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(level)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    logging.info(f"Logging to {log_file}")
    return log_file

class TTSLogger:
    """Logger class for redirecting stdout to the log file."""
    
    def __init__(self, log_file):
        """
        Initialize the logger.
        
        Args:
            log_file (str): Path to the log file.
        """
        self.log_file = log_file
        self.original_stdout = sys.stdout

    def write(self, text):
        """
        Write text to the log file and stdout.
        
        Args:
            text (str): Text to write.
        """
        if text.strip():  # Only log non-empty lines
            logging.debug(text.strip())
        self.original_stdout.write(text)  # Still show progress in terminal

    def flush(self):
        """Flush the output."""
        self.original_stdout.flush()

def show_notification(title, message):
    """
    Show a desktop notification.
    
    Args:
        title (str): Notification title.
        message (str): Notification message.
    """
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            apple_script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', apple_script], check=True)
            
        elif system == "Windows":
            # Use PowerShell to show notification on Windows
            ps_script = f'[System.Windows.Forms.MessageBox]::Show("{message}", "{title}")'
            subprocess.run(
                ["powershell", "-c", ps_script],
                check=True
            )
            
        elif system == "Linux":
            # Use notify-send on Linux
            subprocess.run(['notify-send', title, message], check=True)
            
        else:
            logging.warning(f"Notifications not supported on {system}")
            
    except Exception as e:
        logging.error(f"Error showing notification: {e}")

def check_dependencies(required_packages):
    """
    Check if required packages are installed.
    
    Args:
        required_packages (list): List of required package names.
        
    Returns:
        tuple: (missing_packages, outdated_packages)
    """
    import pkg_resources
    import importlib
    
    missing_packages = []
    outdated_packages = []
    
    for package in required_packages:
        try:
            # Try to import the package
            importlib.import_module(package.replace('-', '_'))
            
            # Check installed version
            try:
                installed_version = pkg_resources.get_distribution(package).version
                logging.info(f"✓ {package} (version {installed_version})")
            except pkg_resources.DistributionNotFound:
                missing_packages.append(package)
                logging.warning(f"✗ {package} not found")
                
        except ImportError:
            missing_packages.append(package)
            logging.warning(f"✗ {package} not found")
    
    return missing_packages, outdated_packages

def install_package(package):
    """
    Install a Python package using pip.
    
    Args:
        package (str): Package name to install.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        logging.info(f"Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing {package}: {e}")
        return False 