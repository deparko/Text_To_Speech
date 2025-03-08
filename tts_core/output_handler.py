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
    
    def _get_output_paths(self, format_ext: str) -> Tuple[Path, Path, Path, Path]:
        """
        Generate paths for output files.
        
        Args:
            format_ext: The audio file format extension
            
        Returns:
            Tuple of (audio_path, text_path, srt_path, html_path)
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_path = self.output_dir / f'tts_{timestamp}'
        
        audio_path = base_path.with_suffix(f'.{format_ext}')
        text_path = base_path.with_suffix('.md')
        srt_path = base_path.with_suffix('.srt')
        html_path = base_path.with_suffix('.html')
        
        return audio_path, text_path, srt_path, html_path
    
    def _generate_html_viewer(self, html_path: Path, audio_path: Path, segments: List[str], duration: float):
        """
        Generate an HTML viewer for the audio and text content.
        
        Args:
            html_path: Path to save the HTML file
            audio_path: Path to the audio file
            segments: List of text segments
            duration: Total duration in seconds
        """
        try:
            # Read the template
            template_path = Path(__file__).parent / 'viewer_template.html'
            logging.info(f"Looking for template at: {template_path}")
            
            if not template_path.exists():
                raise FileNotFoundError(f"HTML template not found at {template_path}")
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            
            # Prepare segment data
            current_time = 0.0
            segment_data = []
            
            for segment in segments:
                segment_duration = len(segment) / self.char_rate
                timestamp = self._format_timestamp(current_time).replace(',', '.')
                
                segment_data.append({
                    'startTime': current_time,
                    'endTime': current_time + segment_duration,
                    'timestamp': timestamp,
                    'text': segment,
                    'preview': segment[:50] + "..." if len(segment) > 50 else segment,
                    'isQuote': segment.count('"') >= 2
                })
                
                current_time += segment_duration
            
            # Prepare metadata
            metadata = {
                'generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'audioFile': audio_path.name,
                'voice': self.config.get('openai', 'voice', 'default'),
                'duration': str(timedelta(seconds=int(duration))),
                'wordCount': f"{len(' '.join(segments).split()):,}",
                'readingTime': f"{duration / 60:.1f}"
            }
            
            # Convert Python objects to JSON-compatible strings
            data_injection = f'const audioData = {{\n            metadata: {json.dumps(metadata)},\n            segments: {json.dumps(segment_data)}\n        }};'
            
            # Insert data into template
            html_content = template.replace(
                'const audioData = {\n            metadata: {},\n            segments: []\n        };',
                data_injection
            )
            
            # Save the HTML file
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logging.info(f"Created HTML viewer: {html_path}")
            
        except Exception as e:
            logging.error(f"Error generating HTML viewer: {str(e)}")
            logging.error(f"Template path: {template_path}")
            logging.error(f"Current directory: {os.getcwd()}")
            raise  # Re-raise the exception after logging
    
    def save_audio(self, audio_data, format_ext, original_text=None):
        """
        Save audio data to a file and create accompanying SRT, markdown, and HTML files.
        
        Args:
            audio_data (bytes): The audio data to save
            format_ext (str): The file format extension (e.g., 'mp3', 'wav')
            original_text (str, optional): The original text for creating SRT and markdown
            
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
        
        # Generate new files
        audio_path, text_path, srt_path, html_path = self._get_output_paths(format_ext)
        
        # Save audio file
        with open(audio_path, 'wb') as f:
            f.write(audio_data)
        
        # Create accompanying files if text is provided
        if original_text:
            # Split text into segments
            segments = self._split_into_segments(original_text)
            duration = sum(len(segment) / self.char_rate for segment in segments)
            
            # Create markdown file
            self._save_text_file(text_path, original_text, audio_path.name)
            
            # Create SRT file
            srt_content, _ = self._create_srt_content(original_text)
            with open(srt_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            # Create HTML viewer
            self._generate_html_viewer(html_path, audio_path, segments, duration)
            
            logging.info(f"Created SRT file: {srt_path}")
        
        # Cache if enabled
        if self.use_cache:
            with open(cache_path, 'wb') as f:
                f.write(audio_data)
            logging.info(f"Audio cached for future use: {cache_path}")
        
        return self._process_audio_file(audio_path, format_ext)
    
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
    
    def _save_text_file(self, text_path: Path, text: str, audio_filename: str):
        """
        Save the text content in markdown format with enhanced metadata and formatting.
        
        Args:
            text_path: Path to save the text file
            text: The text content
            audio_filename: Name of the associated audio file
        """
        # Calculate metadata
        word_count = len(text.split())
        char_count = len(text)
        reading_time = word_count / 150  # Assuming 150 words per minute
        duration = char_count / self.char_rate  # Using our established character rate
        
        with open(text_path, 'w', encoding='utf-8') as f:
            # Write header with enhanced metadata
            f.write("# Text to Speech Output\n\n")
            f.write("## Metadata\n\n")
            f.write(f"- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"- **Audio File**: [{audio_filename}]({audio_filename})\n")
            f.write(f"- **Voice**: {self.config.get('openai', 'voice', 'default')}\n")
            f.write(f"- **Duration**: {timedelta(seconds=int(duration))}\n")
            f.write(f"- **Word Count**: {word_count:,} words\n")
            f.write(f"- **Reading Time**: {reading_time:.1f} minutes\n\n")
            
            f.write("## Table of Contents\n\n")
            
            # Split text into segments and create TOC
            segments = self._split_into_segments(text)
            current_time = 0.0
            
            for i, segment in enumerate(segments, 1):
                segment_duration = len(segment) / self.char_rate
                timestamp = self._format_timestamp(current_time).replace(',', '.')
                preview = segment[:50] + "..." if len(segment) > 50 else segment
                f.write(f"{i}. [{timestamp}] {preview}\n")
                current_time += segment_duration
            
            f.write("\n---\n\n")
            f.write("## Content\n\n")
            
            # Write the content with timestamps and formatted quotes
            current_time = 0.0
            for i, segment in enumerate(segments, 1):
                timestamp = self._format_timestamp(current_time).replace(',', '.')
                
                # Format quotes properly
                formatted_segment = segment
                if segment.count('"') >= 2:
                    formatted_segment = f">{formatted_segment}"
                
                f.write(f"### [{timestamp}] Segment {i}\n\n{formatted_segment}\n\n")
                current_time += len(segment) / self.char_rate
            
            # Add footer with navigation help
            f.write("\n---\n\n")
            f.write("## Navigation\n\n")
            f.write("- Click on timestamps to jump to that section in the audio file (when viewed in the HTML player)\n")
            f.write("- Quoted text is indicated with '>' at the beginning of the line\n")
            f.write("- Use the table of contents to quickly navigate to different segments\n")
        
        logging.info(f"Created enhanced markdown file: {text_path}")
    
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