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


class VideoAnalyzer:
    """Process video files to extract frame-accurate transcription data with speaker detection."""
    
    # AssemblyAI API base URL
    BASE_URL = "https://api.assemblyai.com/v2"
    
    def __init__(self, assemblyai_api_key: Optional[str] = None):
        """
        Initialize the VideoAnalyzer.
        
        Args:
            assemblyai_api_key: AssemblyAI API key. If None, will use ASSEMBLYAI_API_KEY environment variable.
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
        """
        Extract audio from video file to a temporary file.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Path to the extracted audio file
            
        Raises:
            RuntimeError: If audio extraction fails
        """
        logger.info(f"Extracting audio from: {video_path}")
        
        try:
            # Create a temporary file for the audio
            audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            audio_path = audio_file.name
            audio_file.close()
            
            # Extract audio using ffmpeg
            (
                ffmpeg.input(video_path)
                .output(audio_path, acodec='libmp3lame', ac=1, ar='16k')
                .overwrite_output()
                .run(quiet=True)
            )
            
            # Get file size and log it
            file_size_bytes = os.path.getsize(audio_path)
            file_size_mb = file_size_bytes / (1024 * 1024)
            logger.info(f"Extracted audio file size: {file_size_mb:.2f} MB ({file_size_bytes} bytes)")
            
            logger.info(f"Audio extracted to: {audio_path}")
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
        """
        Transcribe audio using AssemblyAI with speaker diarization.
        
        Args:
            audio_url: The URL of the uploaded audio file
            custom_spell: Optional list of custom spellings
            
        Returns:
            Transcription result with word-level timestamps and speaker labels
        """
        logger.info(f"Submitting transcription request to AssemblyAI")
        
        # Create transcription request
        endpoint = f"{self.BASE_URL}/transcript"
        
        json_data = {
            "audio_url": audio_url,
            "speaker_labels": True,  # Enable speaker diarization
            "format_text": True,     # Add punctuation and formatting
            "punctuate": True,       # Add punctuation
            "word_boost": [],        # No word boost
            "dual_channel": False    # Single channel audio
        }
        
        # Add custom spellings if provided
        if custom_spell:
            json_data["custom_spelling"] = custom_spell
        
        # Submit transcription request
        response = requests.post(endpoint, json=json_data, headers=self.headers)
        
        if response.status_code != 200:
            error_message = f"Transcription request failed: {response.text}"
            logger.error(error_message)
            raise RuntimeError(error_message)
            
        transcript_id = response.json()["id"]
        logger.info(f"Transcription request submitted successfully. ID: {transcript_id}")
        
        # Poll for transcription completion
        polling_endpoint = f"{endpoint}/{transcript_id}"
        
        while True:
            polling_response = requests.get(polling_endpoint, headers=self.headers)
            polling_response_json = polling_response.json()
            
            status = polling_response_json["status"]
            logger.info(f"Transcription status: {status}")
            
            if status == "completed":
                logger.info("Transcription completed successfully!")
                return polling_response_json
            elif status == "error":
                error_message = f"Transcription failed: {polling_response_json.get('error', 'Unknown error')}"
                logger.error(error_message)
                raise RuntimeError(error_message)
            else:
                # Wait for a few seconds before polling again
                logger.info("Waiting for transcription to complete...")
                time.sleep(5)
    
    def process_transcript_to_words(self, transcript_data: Dict[str, Any], fps: float) -> Tuple[List[str], str, List[Dict[str, Any]]]:
        """
        Process AssemblyAI transcript data to extract speakers, full transcript, and word-level data.
        
        Args:
            transcript_data: The transcription result from AssemblyAI
            fps: Frames per second of the video
            
        Returns:
            Tuple of (list of unique speakers, full transcript text, list of words with frame data)
        """
        # Get the full transcript text
        full_transcript = transcript_data.get("text", "")
        
        # Get the words with speaker labels and timestamps
        words_data = transcript_data.get("words", [])
        
        # Extract unique speakers
        speakers_set = set()
        for word_data in words_data:
            speaker = word_data.get("speaker", "speaker")
            # Clean up speaker label to be consistent (e.g., "A" instead of "speaker_A")
            if speaker.startswith("speaker_"):
                speaker = speaker.replace("speaker_", "Speaker ")
            speakers_set.add(speaker)
        
        speakers = sorted(list(speakers_set))
        
        # Process words with frame data
        processed_words = []
        for word_data in words_data:
            word = word_data.get("text", "").strip()
            if not word:  # Skip empty words
                continue
                
            # Get timestamps in milliseconds and convert to seconds
            start_time_ms = word_data.get("start", 0)
            end_time_ms = word_data.get("end", 0)
            start_time_sec = start_time_ms / 1000
            end_time_sec = end_time_ms / 1000
            
            # Get speaker (clean up speaker label)
            speaker = word_data.get("speaker", "speaker")
            if speaker.startswith("speaker_"):
                speaker = speaker.replace("speaker_", "Speaker ")
            
            # Convert time to frames
            frame_in = round(start_time_sec * fps)
            frame_out = round(end_time_sec * fps)
            
            # Ensure frame_out is at least one frame after frame_in
            if frame_out <= frame_in:
                frame_out = frame_in + 1
            
            processed_words.append({
                "word": word,
                "speaker": speaker,
                "frame_in": frame_in,
                "frame_out": frame_out
            })
        
        return speakers, full_transcript, processed_words
    
    def process_video(self, video_path: str, custom_spell: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Process a video file: extract metadata, transcribe, and format results.
        
        Args:
            video_path: Path to the video file
            custom_spell: Optional list of custom spellings
            
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
                
                # Step 5: Process transcript to extract speakers and word-level data
                speakers, full_transcript, processed_words = self.process_transcript_to_words(
                    transcription_result, fps
                )
                
                # Build the final result
                result = {
                    "file_name": file_name,
                    "fps": fps,
                    "duration_frames": duration_frames,
                    "speakers": speakers,
                    "full_transcript": full_transcript,
                    "words": processed_words
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
                custom_spell: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Analyze a video file and save the results to a JSON file.
        
        Args:
            video_path: Path to the video file
            output_path: Path to save the output JSON. If None, uses video_path + '.transcript.json'
            custom_spell: Optional list of custom spellings to apply
            
        Returns:
            The generated transcript data
            
        Raises:
            FileNotFoundError: If the video file doesn't exist
        """
        # Check if the file exists
        if not os.path.isfile(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Process the video
        result = self.process_video(video_path, custom_spell)
        
        # Determine output path if not provided
        if output_path is None:
            output_path = f"{video_path}.transcript.json"
        
        # Write results to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Transcript saved to: {output_path}")
        
        # Return non-zero exit code on error
        if "error" in result:
            exit(1)
            
        return result


def main():
    """Command-line entry point for video analysis."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Video frame-based transcript analyzer using AssemblyAI")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("--output", "-o", help="Path to save the output JSON")
    parser.add_argument("--api-key", help="AssemblyAI API key (defaults to ASSEMBLYAI_API_KEY env var)")
    parser.add_argument("--custom-spell", help="JSON file containing custom spellings", type=str)
    
    args = parser.parse_args()
    
    try:
        # Load custom spellings if provided
        custom_spell = None
        if args.custom_spell:
            with open(args.custom_spell, 'r') as f:
                custom_spell = json.load(f)
        
        analyzer = VideoAnalyzer(assemblyai_api_key=args.api_key)
        analyzer.analyze(args.video_path, args.output, custom_spell)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
