"""
Input handling for the Text-to-Speech application.
This module provides functions for getting text from various sources.
"""

import os
import pyperclip
import logging
import mimetypes
import re

class InputHandler:
    """Handles different input sources for text."""
    
    @staticmethod
    def clean_text(text):
        """
        Clean text by removing problematic characters and normalizing whitespace.
        
        Args:
            text (str): The text to clean.
            
        Returns:
            str: The cleaned text.
        """
        if not text:
            return ""
            
        # Only remove truly problematic characters
        text = re.sub(r'[\x00-\x1F\x7F]', '', text)
        
        # Normalize whitespace (only multiple spaces/newlines)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    @staticmethod
    def from_clipboard():
        """
        Get text from the clipboard.
        
        Returns:
            str: The text from the clipboard, or empty string if clipboard is empty.
        """
        try:
            text = pyperclip.paste().strip()
            if text:
                logging.info(f"Got {len(text)} characters from clipboard")
            else:
                logging.warning("Clipboard is empty")
            return text
        except Exception as e:
            logging.error(f"Error getting text from clipboard: {e}")
            return ""
    
    @staticmethod
    def from_file(file_path):
        """
        Read text from a file based on its extension.
        
        Args:
            file_path (str): Path to the file to read.
            
        Returns:
            str: The text from the file, or None if the file could not be read.
        """
        if not os.path.exists(file_path):
            logging.error(f"File {file_path} not found")
            return None
            
        # Get file extension and mime type
        file_ext = os.path.splitext(file_path)[1].lower()
        mime_type, _ = mimetypes.guess_type(file_path)
        
        logging.info(f"Reading file: {file_path} (type: {mime_type or file_ext})")
        
        # Handle different file types
        try:
            if file_ext == '.txt' or mime_type == 'text/plain':
                # Simple text file
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    logging.info(f"Read {len(text)} characters from text file")
                    return text
                    
            elif file_ext == '.pdf':
                # PDF file
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() + "\n"
                        logging.info(f"Read {len(text)} characters from PDF file ({len(reader.pages)} pages)")
                        return text
                except ImportError:
                    logging.error("PyPDF2 module not found. Please install it with: pip install PyPDF2")
                    return None
                    
            elif file_ext in ['.docx', '.doc']:
                # Word document
                try:
                    import docx
                    doc = docx.Document(file_path)
                    text = "\n".join([para.text for para in doc.paragraphs])
                    logging.info(f"Read {len(text)} characters from Word document ({len(doc.paragraphs)} paragraphs)")
                    return text
                except ImportError:
                    logging.error("python-docx module not found. Please install it with: pip install python-docx")
                    return None
                    
            else:
                logging.error(f"Unsupported file format: {file_ext}")
                logging.info("Supported formats: .txt, .pdf, .docx, .doc")
                return None
                
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return None
    
    @staticmethod
    def get_text(file_path=None, text=None):
        """
        Get text from the specified source.
        
        Args:
            file_path (str, optional): Path to a file to read.
            text (str, optional): Direct text input.
            
        Returns:
            str: The text from the specified source, or None if no text could be obtained.
        """
        # Priority: direct text > file > clipboard
        if text:
            logging.info(f"Using provided text ({len(text)} characters)")
            return InputHandler.clean_text(text)
            
        if file_path:
            text = InputHandler.from_file(file_path)
            if text:
                return InputHandler.clean_text(text)
            
        clipboard_text = InputHandler.from_clipboard()
        if clipboard_text:
            return InputHandler.clean_text(clipboard_text)
            
        logging.error("No text provided, file is empty, or clipboard is empty")
        return None 