"""
Input handling for the Text-to-Speech application.
"""

import os
import re
import logging
import pyperclip
from pathlib import Path
from typing import Optional

class InputHandler:
    """Handles text input from various sources."""
    
    def __init__(self):
        """Initialize the input handler."""
        self.supported_extensions = {'.txt', '.md', '.rtf', '.doc', '.docx', '.pdf'}
    
    def from_clipboard(self) -> str:
        """
        Get text from clipboard.
        
        Returns:
            str: The text from clipboard, or empty string if clipboard is empty.
        """
        try:
            text = pyperclip.paste()
            if not text:
                logging.warning("Clipboard is empty")
                return ""
            return text
        except Exception as e:
            logging.error(f"Error reading from clipboard: {e}")
            return ""
    
    def from_file(self, file_path: str) -> str:
        """
        Read text from a file.
        
        Args:
            file_path (str): Path to the file to read.
        
        Returns:
            str: The text content of the file, or empty string if file cannot be read.
        """
        path = Path(file_path)
        if not path.exists():
            logging.error(f"File not found: {file_path}")
            return ""
            
        if path.suffix.lower() not in self.supported_extensions:
            logging.error(f"Unsupported file type: {path.suffix}")
            return ""
            
        try:
            # Handle different file types
            suffix = path.suffix.lower()
            
            # Text files (txt, md, rtf)
            if suffix in {'.txt', '.md', '.rtf'}:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            # PDF files
            elif suffix == '.pdf':
                try:
                    import PyPDF2
                    text = []
                    with open(path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        for page in reader.pages:
                            text.append(page.extract_text())
                    return '\n'.join(text)
                except ImportError:
                    logging.error("PyPDF2 not installed. Install with: pip install PyPDF2")
                    return ""
            
            # Word documents
            elif suffix in {'.doc', '.docx'}:
                try:
                    from docx import Document
                    doc = Document(path)
                    return '\n'.join(paragraph.text for paragraph in doc.paragraphs)
                except ImportError:
                    logging.error("python-docx not installed. Install with: pip install python-docx")
                    return ""
            
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text for TTS processing.
        
        Args:
            text (str): The text to clean.
        
        Returns:
            str: The cleaned text.
        """
        if not text:
            return ""
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common punctuation issues
        text = re.sub(r'\.{3,}', '...', text)  # Normalize ellipsis
        text = re.sub(r'["\']', '"', text)     # Normalize quotes
        text = re.sub(r'[-‐‑‒–—―]', '-', text) # Normalize hyphens/dashes
        
        # Add space after punctuation if missing
        text = re.sub(r'([.!?])([A-Za-z])', r'\1 \2', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+\.\S+', '', text)
        
        # Remove special characters
        text = re.sub(r'[^\w\s.,!?;:"\'-]', ' ', text)
        
        # Clean up final result
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

def get_input_text(text: Optional[str] = None, file_path: Optional[str] = None) -> str:
    """
    Get input text from either direct text input or file.
    
    Args:
        text (str, optional): Direct text input
        file_path (str, optional): Path to input file
        
    Returns:
        str: The input text
    """
    handler = InputHandler()
    
    if text:
        return handler.clean_text(text)
    elif file_path:
        return handler.clean_text(handler.from_file(file_path))
    else:
        return handler.clean_text(handler.from_clipboard()) 