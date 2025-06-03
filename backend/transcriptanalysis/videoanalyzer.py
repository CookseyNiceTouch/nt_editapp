#!/usr/bin/env python3
"""
VideoAnalyzer - A tool for generating frame-based transcription data from video files.

This module ingests a video file, extracts audio, uses AssemblyAI to generate
a transcript with speaker detection, and outputs a JSON dataset with words
keyed by frame counts.
"""

import json
import os
import logging
import tempfile
import re
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path

import ffmpeg
from dotenv import load_dotenv

# Load environment variables from .env file (for API keys)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%SZ'
)
logger = logging.getLogger(__name__)


class ProjectBriefParser:
    """Parse project brief files to extract contextual information for transcription accuracy."""
    
    def __init__(self, brief_path: Optional[str] = None):
        """Initialize with optional brief file path."""
        self.brief_path = brief_path
        self.brief_content = ""
        self.parsed_data = {}
        
        if brief_path and os.path.exists(brief_path):
            self.load_brief(brief_path)
    
    def load_brief(self, brief_path: str) -> None:
        """Load and parse the brief file."""
        try:
            with open(brief_path, 'r', encoding='utf-8') as f:
                self.brief_content = f.read()
            
            self.parsed_data = self._parse_brief_content(self.brief_content)
            logger.info(f"Loaded project brief from: {brief_path}")
            
        except Exception as e:
            logger.warning(f"Could not load brief file {brief_path}: {e}")
            self.parsed_data = {}
    
    def _parse_brief_content(self, content: str) -> Dict[str, Any]:
        """Extract relevant information from brief content."""
        parsed = {
            "speakers": [],
            "custom_vocabulary": [],
            "custom_spellings": [],
            "expected_speakers": 0,
            "project_context": {}
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Extract key information patterns
            if 'talent:' in line.lower() or 'speakers:' in line.lower():
                # Extract speaker names
                speakers = self._extract_speakers(line)
                parsed["speakers"].extend(speakers)
                
            elif 'title:' in line.lower():
                title = self._extract_title(line)
                if title:
                    parsed["custom_vocabulary"].extend(title.split())
                    
            elif 'objective:' in line.lower():
                current_section = 'objective'
                
            elif 'core message:' in line.lower():
                current_section = 'core_message'
                
            elif current_section and line and not line.endswith(':'):
                # Extract vocabulary from content sections
                vocab = self._extract_vocabulary_from_text(line)
                parsed["custom_vocabulary"].extend(vocab)
        
        # Clean and deduplicate
        parsed["speakers"] = list(set([s.title() for s in parsed["speakers"] if s]))
        parsed["expected_speakers"] = len(parsed["speakers"]) if parsed["speakers"] else 0
        parsed["custom_vocabulary"] = list(set([v.lower() for v in parsed["custom_vocabulary"] if len(v) > 2]))
        
        # Generate custom spellings from speaker names
        for speaker in parsed["speakers"]:
            parsed["custom_spellings"].append({
                "from": [speaker.lower(), speaker.upper()],
                "to": speaker
            })
        
        return parsed
    
    def _extract_speakers(self, line: str) -> List[str]:
        """Extract speaker names from talent/speaker line."""
        # Remove the label part
        content = re.sub(r'^[^:]*:', '', line).strip()
        
        # Split by common separators
        speakers = re.split(r'[,&+/]|\band\b', content)
        
        # Clean up speaker names
        cleaned_speakers = []
        for speaker in speakers:
            speaker = re.sub(r'[^\w\s]', '', speaker).strip()
            if speaker and len(speaker) > 1:
                cleaned_speakers.append(speaker)
        
        return cleaned_speakers
    
    def _extract_title(self, line: str) -> str:
        """Extract title from title line."""
        # Remove quotes and title prefix
        title = re.sub(r'^[^:]*:', '', line).strip()
        title = re.sub(r'^["\']|["\']$', '', title).strip()
        return title
    
    def _extract_vocabulary_from_text(self, text: str) -> List[str]:
        """Extract important vocabulary from text content."""
        # Remove common words and extract meaningful terms
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        
        # Extract words, prioritize quoted terms and proper nouns
        words = []
        
        # Extract quoted terms (high priority)
        quoted_terms = re.findall(r'"([^"]+)"', text)
        for term in quoted_terms:
            words.extend(term.split())
        
        # Extract capitalized terms (likely proper nouns)
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
        words.extend(capitalized)
        
        # Extract other meaningful words
        all_words = re.findall(r'\b\w+\b', text.lower())
        meaningful_words = [w for w in all_words if w not in common_words and len(w) > 3]
        words.extend(meaningful_words)
        
        return words
    
    def get_transcription_config(self) -> Dict[str, Any]:
        """Get configuration for enhanced transcription based on brief."""
        if not self.parsed_data:
            return {}
            
        config = {}
        
        # Speaker configuration
        if self.parsed_data.get("expected_speakers", 0) > 0:
            config["speakers_expected"] = self.parsed_data["expected_speakers"]
        
        # Word boost vocabulary
        if self.parsed_data.get("custom_vocabulary"):
            config["word_boost"] = self.parsed_data["custom_vocabulary"][:50]  # Limit to 50 terms
        
        # Custom spellings
        if self.parsed_data.get("custom_spellings"):
            config["custom_spelling"] = self.parsed_data["custom_spellings"]
        
        return config
    
    def get_speaker_mapping(self) -> Dict[str, str]:
        """Get mapping from detected speakers to expected speakers."""
        if not self.parsed_data.get("speakers"):
            return {}
        
        # Create mapping from A, B, C... to actual names
        speaker_names = self.parsed_data["speakers"]
        mapping = {}
        
        for i, name in enumerate(speaker_names):
            letter = chr(65 + i)  # A, B, C...
            mapping[letter] = name
            mapping[f"Speaker {letter}"] = name
            mapping[f"speaker_{letter}".lower()] = name
        
        return mapping


class VideoAnalyzer:
    """Process video files to extract frame-accurate transcription data with speaker detection."""
    
    # AssemblyAI API base URL
    BASE_URL = "https://api.assemblyai.com/v2"
    
    def __init__(self, assemblyai_api_key: Optional[str] = None, brief_path: Optional[str] = None):
        """
        Initialize the VideoAnalyzer.
        
        Args:
            assemblyai_api_key: AssemblyAI API key. If None, will use ASSEMBLYAI_API_KEY environment variable.
            brief_path: Path to project brief file for context enhancement
        """
        # Set AssemblyAI API key from args or environment
        self.api_key = assemblyai_api_key or os.environ.get("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("AssemblyAI API key must be provided either as an argument or via ASSEMBLYAI_API_KEY environment variable")
        
        # Initialize headers for API requests
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Initialize brief parser
        self.brief_parser = ProjectBriefParser(brief_path)
        
        if self.brief_parser.parsed_data:
            logger.info(f"Brief loaded - Expected speakers: {self.brief_parser.parsed_data.get('speakers', 'Unknown')}")

    def probe_video_file(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from video file using ffprobe.
        
        Args:
            file_path: Path to the video file
            
        Returns:
            Dict containing fps and duration information
            
        Raises:
            RuntimeError: If ffprobe fails or required metadata is missing
        """
        logger.info(f"Probing video file: {file_path}")
        
        try:
            probe = ffmpeg.probe(file_path)
            
            # Get video stream info
            video_stream = next((stream for stream in probe['streams'] 
                               if stream['codec_type'] == 'video'), None)
            
            if not video_stream:
                raise RuntimeError("No video stream found in the file")
            
            # Extract framerate
            fps_parts = video_stream.get('r_frame_rate', '').split('/')
            if len(fps_parts) == 2 and fps_parts[1] != '0':
                fps = float(fps_parts[0]) / float(fps_parts[1])
            else:
                # Fallback to avg_frame_rate if r_frame_rate is not available
                fps_parts = video_stream.get('avg_frame_rate', '').split('/')
                if len(fps_parts) == 2 and fps_parts[1] != '0':
                    fps = float(fps_parts[0]) / float(fps_parts[1])
                else:
                    raise RuntimeError("Could not determine video frame rate")
            
            # Get duration in seconds
            duration_seconds = float(video_stream.get('duration', probe.get('format', {}).get('duration', 0)))
            
            if duration_seconds <= 0:
                raise RuntimeError("Invalid video duration detected")
            
            # Get audio stream info for speech estimation
            audio_stream = next((stream for stream in probe['streams'] 
                               if stream['codec_type'] == 'audio'), None)
            
            # Calculate total frames
            duration_frames = round(duration_seconds * fps)
            
            result = {
                "fps": fps,
                "duration_seconds": duration_seconds,
                "duration_frames": duration_frames,
                "has_audio": audio_stream is not None
            }
            
            logger.info(f"Video metadata: fps={fps}, duration={duration_seconds}s, frames={duration_frames}")
            return result
            
        except ffmpeg.Error as e:
            error_message = f"ffprobe error: {str(e)}"
            logger.error(error_message)
            raise RuntimeError(error_message)
    
    def extract_audio(self, video_path: str) -> str:
        """Extract audio with optimal settings for transcription accuracy."""
        logger.info(f"Extracting audio from: {video_path}")
        
        try:
            # Create temporary file for high-quality audio
            audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            audio_path = audio_file.name
            audio_file.close()
            
            # Get source audio properties first
            probe = ffmpeg.probe(video_path)
            audio_stream = next((stream for stream in probe['streams'] 
                               if stream['codec_type'] == 'audio'), None)
            
            if not audio_stream:
                raise RuntimeError("No audio stream found")
            
            # Determine optimal sample rate (prefer source rate up to 48kHz)
            source_rate = int(audio_stream.get('sample_rate', 44100))
            optimal_rate = min(source_rate, 48000)  # Cap at 48kHz
            optimal_rate = max(optimal_rate, 22050)  # Minimum 22kHz for quality
            
            # Extract with optimal settings
            stream = ffmpeg.input(video_path)
            
            # Apply audio filters for cleanup
            audio = stream.audio.filter('highpass', f=80)  # Remove low-frequency noise
            audio = audio.filter('lowpass', f=8000)        # Remove high-frequency noise
            audio = audio.filter('volume', '1.5')          # Boost volume slightly
            
            # Output with optimal codec and settings
            out = ffmpeg.output(
                audio, audio_path,
                acodec='pcm_s16le',    # Uncompressed 16-bit PCM
                ac=1,                  # Mono for speaker diarization
                ar=optimal_rate,       # Optimal sample rate
                audio_bitrate='256k'   # High bitrate
            )
            
            ffmpeg.run(out, overwrite_output=True, quiet=True)
            
            # Log quality metrics
            file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
            logger.info(f"Extracted audio: {optimal_rate}Hz, {file_size_mb:.2f}MB")
            
            return audio_path
            
        except ffmpeg.Error as e:
            error_message = f"Audio extraction error: {str(e)}"
            logger.error(error_message)
            raise RuntimeError(error_message)

    def upload_audio_file(self, audio_file_path: str) -> str:
        """
        Upload an audio file to AssemblyAI.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            The URL of the uploaded audio file
        """
        logger.info(f"Uploading audio file to AssemblyAI: {audio_file_path}")
        
        upload_endpoint = f"{self.BASE_URL}/upload"
        
        # Open the audio file in binary mode
        with open(audio_file_path, "rb") as audio_file:
            response = requests.post(
                upload_endpoint,
                headers={"Authorization": self.api_key},
                data=audio_file
            )
            
        if response.status_code != 200:
            error_message = f"Upload failed: {response.text}"
            logger.error(error_message)
            raise RuntimeError(error_message)
            
        upload_url = response.json()["upload_url"]
        logger.info(f"Audio file uploaded successfully: {upload_url}")
        return upload_url

    def transcribe_audio(self, audio_url: str, custom_spell: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Enhanced transcription with project brief integration."""
        logger.info(f"Submitting enhanced transcription request")
        
        endpoint = f"{self.BASE_URL}/transcript"
        
        # Start with base configuration
        json_data = {
            "audio_url": audio_url,
            "speaker_labels": True,
            "format_text": True,
            "punctuate": True,
            "disfluencies": True,           # Keep natural speech patterns
            "speech_model": "best",         # Use highest accuracy model
            "language_code": "en_us",       # Specify language (mutually exclusive with language_detection)
            "boost_param": "high",          # Increase processing power
            "speech_threshold": 0.3,        # Lower threshold for quiet speech
            "dual_channel": False
        }
        
        # Integrate brief-based configuration
        brief_config = self.brief_parser.get_transcription_config()
        json_data.update(brief_config)
        
        # Merge custom spellings
        all_custom_spellings = []
        if custom_spell:
            all_custom_spellings.extend(custom_spell)
        if brief_config.get("custom_spelling"):
            all_custom_spellings.extend(brief_config["custom_spelling"])
        
        if all_custom_spellings:
            json_data["custom_spelling"] = all_custom_spellings
        
        # Log configuration for debugging
        logger.info(f"Transcription config: speakers_expected={json_data.get('speakers_expected', 'auto')}, "
                   f"vocabulary_terms={len(json_data.get('word_boost', []))}, "
                   f"custom_spellings={len(json_data.get('custom_spelling', []))}")
        
        # Submit transcription request
        response = requests.post(endpoint, json=json_data, headers=self.headers)
        
        if response.status_code != 200:
            error_message = f"Transcription request failed: {response.text}"
            logger.error(error_message)
            raise RuntimeError(error_message)
            
        transcript_id = response.json()["id"]
        logger.info(f"Enhanced transcription submitted. ID: {transcript_id}")
        
        # Poll for completion
        return self._poll_transcription(transcript_id)
    
    def _poll_transcription(self, transcript_id: str) -> Dict[str, Any]:
        """Poll for transcription completion with progress tracking."""
        polling_endpoint = f"{self.BASE_URL}/transcript/{transcript_id}"
        start_time = time.time()
        
        while True:
            try:
                response = requests.get(polling_endpoint, headers=self.headers, timeout=30)
                response.raise_for_status()
                result = response.json()
                
                status = result["status"]
                elapsed = time.time() - start_time
                
                logger.info(f"Status: {status} (elapsed: {elapsed:.1f}s)")
                
                if status == "completed":
                    logger.info("Transcription completed successfully!")
                    return result
                elif status == "error":
                    error_msg = result.get('error', 'Unknown error')
                    raise RuntimeError(f"Transcription failed: {error_msg}")
                
                # Progressive backoff
                wait_time = min(5 + (elapsed // 60), 15)
                time.sleep(wait_time)
                
            except requests.RequestException as e:
                logger.warning(f"Polling error: {e}, retrying...")
                time.sleep(10)

    def process_transcript_to_words(self, transcript_data: Dict[str, Any], fps: float, silence_threshold_ms: int = 1000) -> Tuple[List[str], str, List[Dict[str, Any]]]:
        """Enhanced transcript processing with brief-based speaker mapping and silence detection."""
        
        full_transcript = transcript_data.get("text", "")
        words_data = transcript_data.get("words", [])
        
        # Get speaker mapping from brief
        speaker_mapping = self.brief_parser.get_speaker_mapping()
        
        # Track confidence scores
        confidence_scores = [word.get("confidence", 0) for word in words_data if word.get("confidence")]
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        logger.info(f"Average word confidence: {avg_confidence:.3f}")
        if avg_confidence < 0.8:
            logger.warning(f"Low confidence detected ({avg_confidence:.3f}). Consider audio quality improvements.")
        
        # Process speakers and words with silence detection
        speakers_set = set()
        processed_words = []
        
        for i, word_data in enumerate(words_data):
            word = word_data.get("text", "").strip()
            if not word:
                continue
                
            # Enhanced speaker processing with mapping
            raw_speaker = word_data.get("speaker", "Unknown")
            speaker = self._normalize_speaker_label(raw_speaker, speaker_mapping)
            speakers_set.add(speaker)
            
            # Time and frame processing
            start_ms = word_data.get("start", 0)
            end_ms = word_data.get("end", 0)
            
            if end_ms <= start_ms:
                logger.warning(f"Invalid timestamps for word '{word}': {start_ms}-{end_ms}")
                end_ms = start_ms + 200  # Default 200ms duration
            
            frame_in = max(0, round((start_ms / 1000) * fps))
            frame_out = round((end_ms / 1000) * fps)
            
            if frame_out <= frame_in:
                frame_out = frame_in + 1
            
            # Check for silence before this word (except for the first word)
            if i > 0:
                prev_word_data = words_data[i - 1]
                prev_end_ms = prev_word_data.get("end", 0)
                
                # Calculate silence gap
                silence_duration_ms = start_ms - prev_end_ms
                
                if silence_duration_ms >= silence_threshold_ms:
                    # Insert silence marker
                    silence_frame_in = round((prev_end_ms / 1000) * fps)
                    silence_frame_out = frame_in
                    
                    # Ensure silence has at least 1 frame duration
                    if silence_frame_out <= silence_frame_in:
                        silence_frame_out = silence_frame_in + 1
                    
                    processed_words.append({
                        "word": "**SILENCE**",
                        "speaker": "**SILENCE**",
                        "frame_in": silence_frame_in,
                        "frame_out": silence_frame_out,
                        "confidence": 1.0,  # Silence detection is certain
                        "duration_ms": silence_duration_ms
                    })
                    
                    logger.debug(f"Detected silence: {silence_duration_ms}ms between frames {silence_frame_in}-{silence_frame_out}")
                
            # Add the actual word
            processed_words.append({
                "word": word,
                "speaker": speaker,
                "frame_in": frame_in,
                "frame_out": frame_out,
                "confidence": word_data.get("confidence", 0)
            })
        
        speakers = sorted(list(speakers_set))
        
        # Log speaker mapping and silence detection results
        if speaker_mapping:
            logger.info(f"Applied speaker mapping: {speaker_mapping}")
        
        silence_count = len([w for w in processed_words if w["word"] == "**SILENCE**"])
        logger.info(f"Final speakers: {speakers}")
        logger.info(f"Detected {silence_count} silence periods (>{silence_threshold_ms}ms)")
        
        return speakers, full_transcript, processed_words

    def _normalize_speaker_label(self, speaker: str, speaker_mapping: Dict[str, str]) -> str:
        """Normalize speaker labels with brief-based mapping."""
        if not speaker or speaker.lower() == "unknown":
            return "Unknown"
        
        # Clean up AssemblyAI format
        if speaker.startswith("speaker_"):
            letter = speaker.replace("speaker_", "").upper()
            clean_speaker = letter if len(letter) == 1 else f"Speaker {letter}"
        else:
            clean_speaker = speaker.strip()
        
        # Apply mapping from brief if available
        mapped_speaker = speaker_mapping.get(clean_speaker, clean_speaker)
        
        return mapped_speaker

    def process_video(self, video_path: str, custom_spell: Optional[List[Dict[str, Any]]] = None, silence_threshold_ms: int = 1000) -> Dict[str, Any]:
        """
        Process a video file: extract metadata, transcribe, and format results.
        
        Args:
            video_path: Path to the video file
            custom_spell: Optional list of custom spellings
            silence_threshold_ms: Minimum silence duration in milliseconds to mark as silence (default: 1000ms)
            
        Returns:
            Dict containing the complete transcript data in the required format
            
        Raises:
            Various exceptions based on processing stage
        """
        try:
            # Get the filename without path
            file_name = os.path.basename(video_path)
            
            # Step 1: Probe video to get metadata
            metadata = self.probe_video_file(video_path)
            fps = metadata["fps"]
            duration_frames = metadata["duration_frames"]
            
            # Step 2: Extract audio
            audio_path = self.extract_audio(video_path)
            
            try:
                # Step 3: Upload audio to AssemblyAI
                audio_url = self.upload_audio_file(audio_path)
                
                # Step 4: Transcribe audio using AssemblyAI
                transcription_result = self.transcribe_audio(audio_url, custom_spell)
                
                # Step 5: Process transcript to extract speakers, word-level data, and silence detection
                speakers, full_transcript, processed_words = self.process_transcript_to_words(
                    transcription_result, fps, silence_threshold_ms
                )
                
                # Build the final result
                result = {
                    "file_name": file_name,
                    "fps": fps,
                    "duration_frames": duration_frames,
                    "speakers": speakers,
                    "full_transcript": full_transcript,
                    "words": processed_words,
                    "silence_threshold_ms": silence_threshold_ms  # Record the threshold used
                }
                
                logger.info(f"Successfully processed video: {file_name}")
                logger.info(f"Detected speakers: {', '.join(speakers)}")
                return result
                
            finally:
                # Clean up the temporary audio file
                if os.path.exists(audio_path):
                    os.unlink(audio_path)
                    logger.info(f"Removed temporary audio file: {audio_path}")
            
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error processing video: {error_message}")
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            return {
                "error": error_message,
                "timestamp": timestamp
            }
    
    def analyze(self, video_path: str, output_path: Optional[str] = None, 
                custom_spell: Optional[List[Dict[str, Any]]] = None,
                brief_path: Optional[str] = None, silence_threshold_ms: int = 1000) -> Dict[str, Any]:
        """
        Enhanced analyze method with optional brief integration and silence detection.
        
        Args:
            video_path: Path to the video file
            output_path: Path to save the output JSON (if None, saves to project's data/analyzed directory)
            custom_spell: Optional list of custom spellings
            brief_path: Path to project brief file for context
            silence_threshold_ms: Minimum silence duration in milliseconds to mark as silence (default: 1000ms)
        """
        # Load brief if provided and not already loaded
        if brief_path and not self.brief_parser.brief_content:
            self.brief_parser.load_brief(brief_path)
        
        # Check if the file exists
        if not os.path.isfile(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Process the video with silence detection
        result = self.process_video(video_path, custom_spell, silence_threshold_ms)
        
        # Determine output path if not provided - always use analyzed directory
        if output_path is None:
            # Get the directory of this script
            script_dir = Path(__file__).parent
            
            # Navigate to project root (up 2 levels from backend/transcriptanalysis) and then to data/analyzed
            analyzed_dir = script_dir.parent.parent / "data" / "analyzed"
            
            # Ensure the directory exists
            analyzed_dir.mkdir(parents=True, exist_ok=True)
            
            # Create filename from video filename
            video_filename = Path(video_path).stem  # Gets filename without extension
            output_filename = f"{video_filename}.transcript.json"
            output_path = analyzed_dir / output_filename
            
            logger.info(f"Auto-generated output path: {output_path}")
        
        # Write results to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Transcript saved to: {output_path}")
        
        # Return non-zero exit code on error
        if "error" in result:
            exit(1)
            
        return result


def main():
    """Enhanced command-line entry point with brief support and silence detection."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced video transcript analyzer with project brief integration and silence detection")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("--output", "-o", help="Path to save the output JSON")
    parser.add_argument("--api-key", help="AssemblyAI API key (defaults to ASSEMBLYAI_API_KEY env var)")
    parser.add_argument("--custom-spell", help="JSON file containing custom spellings", type=str)
    parser.add_argument("--brief", help="Path to project brief file for enhanced accuracy", type=str)
    parser.add_argument("--silence-threshold", help="Minimum silence duration in milliseconds to mark as silence (default: 1000)", type=int, default=1000)
    
    args = parser.parse_args()
    
    try:
        # Load custom spellings if provided
        custom_spell = None
        if args.custom_spell:
            with open(args.custom_spell, 'r') as f:
                custom_spell = json.load(f)
        
        analyzer = VideoAnalyzer(assemblyai_api_key=args.api_key, brief_path=args.brief)
        analyzer.analyze(args.video_path, args.output, custom_spell, args.brief, args.silence_threshold)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
