"""
Output handling for the Text-to-Speech application.
This module handles audio file output and playback.
"""

import os
import re
import logging
import hashlib
import subprocess
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import sys
from pathlib import Path
import json
from jinja2 import Template

# Import the AIFilenameGenerator
from .ai_filename_generator import AIFilenameGenerator

class OutputHandler:
    """Handles audio output and file management."""
    
    def __init__(self, config):
        """Initialize the output handler with configuration."""
        self.config = config
        
        # Set up output directory (iCloud Drive)
        self.output_dir = Path(os.path.expanduser(config.get("output", "directory", "~/Library/Mobile Documents/com~apple~CloudDocs/TTS_Audio")))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up cache if enabled
        self.use_cache = config.get("output", "cache_audio", False)
        if self.use_cache:
            self.cache_dir = self.output_dir / "cache"
            self.cache_dir.mkdir(exist_ok=True)
            
        # Average speaking rate (characters per second)
        self.char_rate = 15  # Adjustable based on voice speed
        
        # Initialize AI filename generator
        self.ai_filename_generator = AIFilenameGenerator(config)
    
    def get_log_path(self):
        """Get the path for the log file."""
        log_dir = self.output_dir / "logs"
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return log_dir / f"tts_{timestamp}.log"
    
    def _split_into_segments(self, text: str) -> List[str]:
        """
        Split text into segments based on punctuation and length.
        
        Args:
            text (str): The text to split
            
        Returns:
            List[str]: List of text segments
        """
        # Split on sentence endings and other major breaks
        segments = []
        current_segment = []
        
        # Split into sentences first
        sentences = re.split(r'([.!?]+)', text)
        
        for i in range(0, len(sentences)-1, 2):
            sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else '')
            sentence = sentence.strip()
            
            if not sentence:
                continue
                
            # If sentence is too long, split on commas or other breaks
            if len(sentence) > 100:
                subsegments = re.split(r'([,;:])', sentence)
                for j in range(0, len(subsegments)-1, 2):
                    subsegment = subsegments[j] + (subsegments[j+1] if j+1 < len(subsegments) else '')
                    subsegment = subsegment.strip()
                    if subsegment:
                        segments.append(subsegment)
            else:
                segments.append(sentence)
        
        return segments
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Format seconds into SRT timestamp format.
        
        Args:
            seconds (float): Seconds from start
            
        Returns:
            str: Formatted timestamp (HH:MM:SS,mmm)
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        milliseconds = int((seconds % 1) * 1000)
        seconds = int(seconds)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    def _create_srt_content(self, text: str) -> Tuple[str, float]:
        """
        Create SRT content from text.
        
        Args:
            text (str): The text to convert
            
        Returns:
            Tuple[str, float]: SRT content and total duration in seconds
        """
        segments = self._split_into_segments(text)
        srt_lines = []
        current_time = 0.0
        
        for i, segment in enumerate(segments, 1):
            # Calculate duration based on segment length and speaking rate
            duration = len(segment) / self.char_rate
            
            # Minimum duration of 1 second per segment
            duration = max(duration, 1.0)
            
            # Add segment to SRT
            start_time = self._format_timestamp(current_time)
            end_time = self._format_timestamp(current_time + duration)
            
            srt_lines.extend([
                str(i),
                f"{start_time} --> {end_time}",
                segment,
                ""  # Empty line between entries
            ])
            
            current_time += duration
        
        return "\n".join(srt_lines), current_time
    
    def _get_output_paths(self, format_ext: str, base_name: Optional[str] = None) -> Tuple[Path, Path, Path, Path]:
        """
        Generate paths for output files.
        
        Args:
            format_ext: The audio file format extension
            base_name: Optional base name for the files (without extension)
            
        Returns:
            Tuple of (audio_path, text_path, srt_path, html_path)
        """
        if not base_name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_name = f'tts_{timestamp}'
        
        base_path = self.output_dir / base_name
        
        audio_path = base_path.with_suffix(f'.{format_ext}')
        text_path = base_path.with_suffix('.md')
        srt_path = base_path.with_suffix('.srt')
        html_path = base_path.with_suffix('.html')
        
        return audio_path, text_path, srt_path, html_path
    
    def _generate_html_viewer(self, html_path: Path, audio_path: Path, segments: List[str], duration: float, original_text: str = None, processed_text: str = None, prompt_name: str = None):
        """
        Generate an HTML viewer for the audio and text content.
        
        Args:
            html_path: Path to save the HTML file
            audio_path: Path to the audio file
            segments: List of text segments
            duration: Total duration in seconds
            original_text: The original text
            processed_text: The AI-processed text used for speech generation
            prompt_name: The prompt used for AI processing
        """
        try:
            # Find the template file
            template_path = Path(__file__).parent / 'viewer_template.html'
            logging.info(f"Looking for template at: {template_path}")
            
            if not template_path.exists():
                logging.error(f"Template file not found: {template_path}")
                return
            
            # Read the template
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Create Jinja2 template
            template = Template(template_content)
            
            # Prepare segment data
            segment_data = []
            current_time = 0.0
            
            for i, segment in enumerate(segments):
                segment_duration = len(segment) / self.char_rate
                timestamp = self._format_timestamp(current_time)
                
                # Create a preview (first few words)
                words = segment.split()
                preview = ' '.join(words[:5])
                if len(words) > 5:
                    preview += "..."
                
                # Check if segment is a quote
                is_quote = segment.strip().startswith('"') and segment.strip().endswith('"')
                
                segment_data.append({
                    'text': segment,
                    'start': current_time,
                    'end': current_time + segment_duration,
                    'timestamp': timestamp,
                    'preview': preview,
                    'is_quote': is_quote
                })
                
                current_time += segment_duration
            
            # Prepare metadata
            metadata = {
                'duration': str(timedelta(seconds=int(duration))),
                'wordCount': f"{len(' '.join(segments).split()):,}",
                'readingTime': f"{duration / 60:.1f}",
                'originalText': original_text,
                'processedText': processed_text,
                'promptName': prompt_name
            }
            
            # Render the template
            html_content = template.render(
                audio_file=audio_path.name,
                segments=segment_data,
                metadata=metadata
            )
            
            # Write the HTML file
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logging.info(f"Created HTML viewer: {html_path}")
        except Exception as e:
            logging.error(f"Error generating HTML viewer: {str(e)}")
            logging.error(f"Template path: {template_path}")
            logging.error(f"Current directory: {os.getcwd()}")
            raise  # Re-raise the exception after logging
    
    def save_audio(self, audio_data, format_ext, original_text=None, processed_text=None, ai_filename=True, prompt_name=None):
        """
        Save audio data to a file and create accompanying SRT, markdown, and HTML files.
        
        Args:
            audio_data (bytes): The audio data to save
            format_ext (str): The file format extension (e.g., 'mp3', 'wav')
            original_text (str, optional): The original text for creating SRT and markdown
            processed_text (str, optional): The AI-processed text used for speech generation
            ai_filename (bool): Whether to use AI-generated filename
            prompt_name (str, optional): The prompt to use for AI filename generation
            
        Returns:
            str: Path to the saved audio file
        """
        # Check cache first if enabled
        if self.use_cache:
            cache_key = hashlib.md5(audio_data).hexdigest()
            cache_path = self.cache_dir / f"cache_{cache_key}.{format_ext}"
            
            if os.path.exists(cache_path):
                logging.info(f"Using cached audio: {cache_path}")
                return self._process_audio_file(cache_path, format_ext)
        
        # Generate base filename
        base_name = None
        if ai_filename and original_text:
            base_name = self.ai_filename_generator.generate_filename(original_text, prompt_name)
        
        # Generate new files
        audio_path, text_path, srt_path, html_path = self._get_output_paths(format_ext, base_name)
        
        # Save audio file
        with open(audio_path, 'wb') as f:
            f.write(audio_data)
        
        # Create accompanying files if text is provided
        if original_text:
            # Determine which text to use for SRT and timing
            text_for_speech = processed_text if processed_text else original_text
            
            # Split text into segments
            segments = self._split_into_segments(text_for_speech)
            duration = sum(len(segment) / self.char_rate for segment in segments)
            
            # Create markdown file with both original and processed text if available
            self._save_text_file(text_path, original_text, audio_path.name, processed_text, prompt_name)
            
            # Create SRT file using the text that was actually spoken
            srt_content, _ = self._create_srt_content(text_for_speech)
            with open(srt_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            # Create HTML viewer
            self._generate_html_viewer(html_path, audio_path, segments, duration, original_text, processed_text, prompt_name)
            
            logging.info(f"Created SRT file: {srt_path}")
        
        # Cache if enabled
        if self.use_cache:
            cache_path = self.cache_dir / f"cache_{hashlib.md5(audio_data).hexdigest()}.{format_ext}"
            with open(cache_path, 'wb') as f:
                f.write(audio_data)
            logging.info(f"Audio cached for future use: {cache_path}")
        
        return audio_path
    
    def _process_audio_file(self, file_path, format_ext):
        """
        Process the audio file.
        
        Args:
            file_path (str): Path to the audio file
            format_ext (str): The file format extension
            
        Returns:
            str: Path to the processed audio file
        """
        # Only try to add to Music if explicitly enabled
        if self.config.get("output", "add_to_music", False):
            try:
                cmd = ['osascript', '-e', f'tell application "Music" to add POSIX file "{file_path}"']
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    logging.info(f"Added to Music library: {file_path} ({result.stdout.strip()})")
                else:
                    logging.error(f"Error adding to Music library: {result.stderr}")
            except Exception as e:
                logging.error(f"Error adding to Music library: {e}")
        
        return file_path
    
    def play_audio(self, file_path):
        """
        Play an audio file.
        
        Args:
            file_path (str): Path to the audio file to play
        """
        try:
            if os.name == 'posix':  # macOS or Linux
                subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', str(file_path)])
            else:  # Windows
                os.startfile(str(file_path))
        except Exception as e:
            logging.error(f"Error playing audio: {e}")
    
    def _save_text_file(self, text_path: Path, original_text: str, audio_filename: str, processed_text=None, prompt_name=None):
        """
        Save the text content in markdown format with enhanced metadata and formatting.
        
        Args:
            text_path: Path to save the text file
            original_text: The original text
            audio_filename: Name of the associated audio file
            processed_text: The AI-processed text used for speech generation
            prompt_name: The prompt used for AI filename generation
        """
        # Calculate metadata
        word_count = len(original_text.split())
        char_count = len(original_text)
        reading_time = word_count / 150  # Assuming 150 words per minute
        duration = char_count / self.char_rate  # Using our established character rate
        
        try:
            with open(text_path, 'w', encoding='utf-8') as f:
                # Write header with metadata
                f.write(f"# Audio Transcript\n\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"**Audio File:** [{audio_filename}]({audio_filename})\n\n")
                f.write(f"**Duration:** {str(timedelta(seconds=int(duration)))}\n\n")
                f.write(f"**Word Count:** {word_count:,}\n\n")
                f.write(f"**Reading Time:** {reading_time:.1f} minutes\n\n")
                
                if prompt_name and processed_text:
                    f.write(f"**AI Prompt Used:** {prompt_name}\n\n")
                
                # Table of Contents
                f.write("## Table of Contents\n\n")
                
                # Split text into segments and create TOC
                segments = self._split_into_segments(original_text)
                current_time = 0.0
                
                for i, segment in enumerate(segments):
                    segment_duration = len(segment) / self.char_rate
                    timestamp = self._format_timestamp(current_time)
                    
                    # Create a clean segment title (first few words)
                    title_words = segment.split()[:5]
                    title = ' '.join(title_words)
                    if len(title_words) < len(segment.split()):
                        title += "..."
                    
                    f.write(f"- [{timestamp} - {title}](#segment-{i+1})\n")
                    current_time += segment_duration
                
                f.write("\n---\n\n")
                
                # If we have processed text, include both versions
                if processed_text and processed_text != original_text:
                    f.write("## Original Text\n\n")
                    f.write(f"{original_text}\n\n")
                    f.write("## Processed Text\n\n")
                    f.write(f"*Processed with AI prompt: {prompt_name}*\n\n")
                    f.write(f"{processed_text}\n\n")
                    f.write("## Transcript with Timestamps\n\n")
                else:
                    f.write("## Transcript\n\n")
                
                # Write segments with timestamps
                current_time = 0.0
                for i, segment in enumerate(segments):
                    segment_duration = len(segment) / self.char_rate
                    timestamp = self._format_timestamp(current_time)
                    
                    # Check if segment is a quote
                    is_quote = segment.strip().startswith('"') and segment.strip().endswith('"')
                    
                    f.write(f"<a id='segment-{i+1}'></a>\n")
                    f.write(f"**[{timestamp}]** ")
                    
                    if is_quote:
                        f.write(f"> {segment}\n\n")
                    else:
                        f.write(f"{segment}\n\n")
                        
                    current_time += segment_duration
                
            logging.info(f"Created markdown file: {text_path}")
        except Exception as e:
            logging.error(f"Error creating markdown file: {e}")
            raise
    
    def _create_srt(self, srt_path: Path, text: str):
        """Create an SRT subtitle file from the text."""
        # Estimate 150 words per minute for speech
        WORDS_PER_MINUTE = 150
        WORDS_PER_SECOND = WORDS_PER_MINUTE / 60
        
        def format_time(seconds):
            """Format seconds into SRT time format."""
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds = int(seconds % 60)
            milliseconds = int((seconds % 1) * 1000)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
        
        with open(srt_path, 'w', encoding='utf-8') as f:
            # Split into sentences (rough approximation)
            sentences = text.replace('\n', ' ').split('. ')
            current_time = 0
            
            for i, sentence in enumerate(sentences, 1):
                if not sentence.strip():
                    continue
                    
                # Estimate duration based on word count
                words = len(sentence.split())
                duration = words / WORDS_PER_SECOND
                
                # Write SRT entry
                f.write(f"{i}\n")
                f.write(f"{format_time(current_time)} --> {format_time(current_time + duration)}\n")
                f.write(f"{sentence.strip()}.\n\n")
                
                current_time += duration
        
        logging.info(f"Created SRT file: {srt_path}") 