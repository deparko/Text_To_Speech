"""
OpenAI TTS engine implementation.
"""

import os
import re
import io
import logging
import openai
from pathlib import Path
from pydub import AudioSegment

class OpenAITTSEngine:
    """OpenAI Text-to-Speech engine."""
    
    AVAILABLE_VOICES = {
        'nova': 'Female, warm and natural (default)',
        'alloy': 'Neutral and balanced',
        'echo': 'Male, warm and clear',
        'fable': 'Male, British accent',
        'onyx': 'Male, deep and authoritative',
        'shimmer': 'Female, clear and expressive'
    }
    
    MAX_CHARS = 4000  # Slightly less than API limit for safety
    CROSSFADE_DURATION = 100  # milliseconds for crossfade between chunks
    
    # Common abbreviations that shouldn't be treated as sentence endings
    ABBREVIATIONS = r'(?:[A-Za-z]\.){2,}|Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|Sr\.|Jr\.|vs\.|etc\.'
    
    def __init__(self, config):
        """
        Initialize the OpenAI TTS engine.
        
        Args:
            config: Configuration object with OpenAI settings.
        """
        self.config = config
        
        # Get API key from environment or config
        self.api_key = os.getenv('OPENAI_API_KEY') or config.get('openai', 'api_key')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        # Set up client
        openai.api_key = self.api_key
        
        # Get voice settings
        self.voice = config.get('openai', 'voice', 'nova')
        self.model = config.get('openai', 'model', 'tts-1')
        
        if self.voice not in self.AVAILABLE_VOICES:
            logging.warning(f"Invalid voice '{self.voice}', using 'nova'")
            self.voice = 'nova'
    
    def _is_sentence_boundary(self, text: str, pos: int) -> bool:
        """
        Determine if a position in text is a true sentence boundary.
        
        Args:
            text (str): The text to check
            pos (int): Position of potential sentence boundary
            
        Returns:
            bool: True if position is a sentence boundary
        """
        if pos == 0 or pos >= len(text):
            return False
            
        # Check if we're in the middle of an abbreviation
        before = text[max(0, pos-20):pos]
        if re.search(self.ABBREVIATIONS + '$', before):
            return False
            
        # Check for ellipsis
        if text[pos-1:pos+2] == '...':
            return False
            
        # Check if we're inside quotes with more sentence to come
        if '"' in before and '"' not in text[pos:pos+20]:
            return False
            
        return True
    
    def _split_text(self, text: str) -> list[str]:
        """
        Split text into chunks that respect sentence boundaries and API limits.
        
        Args:
            text (str): Text to split
            
        Returns:
            list[str]: List of text chunks
        """
        # Use a more aggressive threshold for longer texts
        total_length = len(text)
        if total_length > self.MAX_CHARS * 2:
            # For very long texts, use 60% of max chars
            CHUNK_THRESHOLD = int(self.MAX_CHARS * 0.6)
        else:
            # For shorter texts, use 80% of max chars
            CHUNK_THRESHOLD = int(self.MAX_CHARS * 0.8)
        
        logging.debug(f"Using chunk threshold of {CHUNK_THRESHOLD} characters for text of length {total_length}")
        
        # Normalize line endings and whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # First find all potential sentence boundaries
        boundaries = []
        for match in re.finditer(r'[.!?]+', text):
            if self._is_sentence_boundary(text, match.end()):
                boundaries.append(match.end())
        
        # Add start and end positions
        boundaries = [0] + boundaries + [len(text)]
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for i in range(len(boundaries) - 1):
            sentence = text[boundaries[i]:boundaries[i+1]].strip()
            
            if not sentence:
                continue
                
            # If sentence alone is too long, split on natural breaks
            if len(sentence) > CHUNK_THRESHOLD:
                # Try splitting on various punctuation marks
                for split_char in ['. ', ', ', '; ', ': ', ' - ', ' ']:
                    subsegments = sentence.split(split_char)
                    max_subsegment = max(len(s.strip()) for s in subsegments)
                    
                    if max_subsegment <= CHUNK_THRESHOLD:
                        for subsegment in subsegments:
                            subsegment = subsegment.strip()
                            if not subsegment:
                                continue
                            
                            # Add the split character back unless it's just a space
                            if split_char.strip():
                                subsegment += split_char.rstrip()
                            
                            if current_length + len(subsegment) > CHUNK_THRESHOLD:
                                if current_chunk:
                                    chunks.append(''.join(current_chunk).strip())
                                current_chunk = [subsegment + ' ']
                                current_length = len(subsegment) + 1
                            else:
                                current_chunk.append(subsegment + ' ')
                                current_length += len(subsegment) + 1
                        break
                else:
                    # If no good splitting point found, split at threshold
                    # but try to break at word boundaries
                    while sentence:
                        if len(sentence) <= CHUNK_THRESHOLD:
                            if current_length + len(sentence) > CHUNK_THRESHOLD:
                                chunks.append(''.join(current_chunk).strip())
                                current_chunk = [sentence + ' ']
                                current_length = len(sentence) + 1
                            else:
                                current_chunk.append(sentence + ' ')
                                current_length += len(sentence) + 1
                            break
                            
                        # Try to find a word boundary near threshold
                        space_pos = sentence.rfind(' ', 0, CHUNK_THRESHOLD)
                        if space_pos == -1:
                            space_pos = CHUNK_THRESHOLD
                            
                        chunk = sentence[:space_pos].strip()
                        if chunk:
                            if current_length + len(chunk) > CHUNK_THRESHOLD:
                                if current_chunk:
                                    chunks.append(''.join(current_chunk).strip())
                                current_chunk = [chunk + ' ']
                                current_length = len(chunk) + 1
                            else:
                                current_chunk.append(chunk + ' ')
                                current_length += len(chunk) + 1
                                
                        sentence = sentence[space_pos:].strip()
            else:
                if current_length + len(sentence) > CHUNK_THRESHOLD:
                    chunks.append(''.join(current_chunk).strip())
                    current_chunk = [sentence + ' ']
                    current_length = len(sentence) + 1
                else:
                    current_chunk.append(sentence + ' ')
                    current_length += len(sentence) + 1
        
        if current_chunk:
            chunks.append(''.join(current_chunk).strip())
            
        # Clean up any double spaces or spaces around quotes
        chunks = [re.sub(r'\s+', ' ', chunk) for chunk in chunks]
        chunks = [re.sub(r'"\s*([^"]+)\s*"', r'" \1 "', chunk) for chunk in chunks]
        chunks = [chunk.strip() for chunk in chunks]
        
        # Verify no chunk exceeds MAX_CHARS
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > self.MAX_CHARS:
                # Emergency split if somehow we still have too long chunks
                words = chunk.split()
                current = []
                current_len = 0
                for word in words:
                    if current_len + len(word) + 1 > self.MAX_CHARS:
                        final_chunks.append(' '.join(current))
                        current = [word]
                        current_len = len(word) + 1
                    else:
                        current.append(word)
                        current_len += len(word) + 1
                if current:
                    final_chunks.append(' '.join(current))
            else:
                final_chunks.append(chunk)
        
        # Log chunk information
        logging.info(f"Split text into {len(final_chunks)} chunks")
        for i, chunk in enumerate(final_chunks):
            logging.debug(f"Chunk {i+1}: {len(chunk)} characters")
            
        return final_chunks
    
    def generate_speech(self, text):
        """
        Generate speech from text using OpenAI's TTS API.
        
        Args:
            text (str): Text to convert to speech.
            
        Returns:
            bytes: Audio data in MP3 format.
        """
        try:
            # Split text into chunks if needed
            chunks = self._split_text(text)
            
            if len(chunks) == 1:
                # Single chunk, direct conversion
                response = openai.audio.speech.create(
                    model=self.model,
                    voice=self.voice,
                    input=chunks[0]
                )
                return response.content
            
            # Multiple chunks, need to combine audio
            audio_segments = []
            total_chunks = len(chunks)
            
            for i, chunk in enumerate(chunks):
                try:
                    logging.info(f"Processing chunk {i+1} of {total_chunks} ({len(chunk)} characters)")
                    response = openai.audio.speech.create(
                        model=self.model,
                        voice=self.voice,
                        input=chunk
                    )
                    
                    # Convert response to AudioSegment
                    audio_data = io.BytesIO(response.content)
                    segment = AudioSegment.from_mp3(audio_data)
                    
                    # Add small silence between chunks to prevent words running together
                    if audio_segments:
                        # Crossfade with previous segment
                        combined = audio_segments[-1].append(segment, crossfade=self.CROSSFADE_DURATION)
                        audio_segments[-1] = combined
                    else:
                        audio_segments.append(segment)
                        
                except Exception as chunk_error:
                    logging.error(f"Error processing chunk {i+1}: {chunk_error}")
                    # Continue with next chunk instead of failing completely
                    continue
            
            if not audio_segments:
                logging.error("No audio segments were successfully generated")
                return None
            
            # Combine all segments
            combined = audio_segments[0]
            
            # Export to bytes
            output = io.BytesIO()
            combined.export(output, format='mp3')
            return output.getvalue()
            
        except Exception as e:
            logging.error(f"Error generating speech with OpenAI TTS: {e}")
            return None
    
    @classmethod
    def list_voices(cls):
        """List available voices with descriptions."""
        print("\nAvailable OpenAI voices:")
        for voice, desc in cls.AVAILABLE_VOICES.items():
            print(f"- {voice}: {desc}")
    
    def get_format(self):
        """Get the audio format (always MP3 for OpenAI TTS)."""
        return "mp3" 