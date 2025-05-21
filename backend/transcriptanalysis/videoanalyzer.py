#!/usr/bin/env python3
"""
VideoAnalyzer - A tool for generating frame-based transcription data from video files.

This module ingests a video file, extracts audio, uses OpenAI Whisper API to generate
a word-level transcript with speaker labels, and outputs a JSON dataset with words
keyed by frame counts.
"""

import json
import os
import logging
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional

import ffmpeg
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%SZ'
)
logger = logging.getLogger(__name__)


class VideoAnalyzer:
    """Process video files to extract frame-accurate transcription data."""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the VideoAnalyzer.
        
        Args:
            openai_api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
        """
        # Set OpenAI API key from args or environment
        if openai_api_key:
            self.client = OpenAI(api_key=openai_api_key)
        else:
            self.client = OpenAI()  # Uses OPENAI_API_KEY from environment
            if not os.environ.get("OPENAI_API_KEY"):
                raise ValueError("OpenAI API key must be provided either as an argument or via OPENAI_API_KEY environment variable")
    
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
            
            # Calculate total frames
            duration_frames = round(duration_seconds * fps)
            
            result = {
                "fps": fps,
                "duration_seconds": duration_seconds,
                "duration_frames": duration_frames
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
    
    def transcribe_audio(self, audio_path: str, prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe audio using OpenAI Whisper API with word-level timestamps.
        
        Args:
            audio_path: Path to the audio file
            prompt: Optional prompt to guide the transcription
            
        Returns:
            Whisper API response containing transcript with word-level timestamps
            
        Raises:
            RuntimeError: If API call fails
        """
        logger.info(f"Submitting audio to Whisper API: {audio_path}")
        
        try:
            # Open the audio file in binary mode
            with open(audio_path, "rb") as audio_file:
                # Call the Whisper API with word-level timestamps
                # Note: For word-level timestamps, we must use whisper-1 model and verbose_json format
                transcription_params = {
                    "model": "whisper-1",
                    "file": audio_file,
                    "response_format": "verbose_json",
                    "timestamp_granularities": ["word"],
                }
                
                # Add prompt if provided
                if prompt:
                    transcription_params["prompt"] = prompt
                
                response = self.client.audio.transcriptions.create(**transcription_params)
            
            logger.info("Successfully received transcript from Whisper API")
            
            # Since response is a Pydantic model, we need to convert it to a dict
            if hasattr(response, "model_dump"):
                # For newer OpenAI Python SDK versions
                return response.model_dump()
            else:
                # For older versions or direct dict access
                return response
            
        except Exception as e:
            error_message = f"Whisper API error: {str(e)}"
            logger.error(error_message)
            raise RuntimeError(error_message)
        finally:
            # Clean up the temporary audio file
            if os.path.exists(audio_path):
                os.unlink(audio_path)
                logger.info(f"Removed temporary audio file: {audio_path}")
    
    def process_video(self, video_path: str, prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a video file: extract metadata, transcribe, and format results.
        
        Args:
            video_path: Path to the video file
            prompt: Optional prompt to guide the transcription
            
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
            
            # Step 3: Transcribe audio
            transcription = self.transcribe_audio(audio_path, prompt)
            
            # Step 4: Process transcript and convert times to frames
            full_transcript = transcription.get("text", "")
            
            # Get words data
            words_data = transcription.get("words", [])
            
            # Extract unique speakers if available
            # Note: Standard Whisper doesn't have speaker labels, so we'll need additional processing
            # for speaker diarization if needed
            speakers = []
            
            # Process words
            processed_words = []
            for word_data in words_data:
                word = word_data.get("word", "").strip()
                if not word:  # Skip empty words
                    continue
                    
                start_time = word_data.get("start", 0)
                end_time = word_data.get("end", 0)
                
                # For now, use "unknown" as speaker since whisper doesn't natively provide speaker labels
                speaker = "speaker1"  # Default to single speaker
                
                # Convert time to frames
                frame_in = round(start_time * fps)
                frame_out = round(end_time * fps)
                
                processed_words.append({
                    "word": word,
                    "speaker": speaker,
                    "frame_in": frame_in,
                    "frame_out": frame_out
                })
                
            # For speaker diarization, we would need to process this separately
            # For now we'll just use a single speaker
            speakers = ["speaker1"]
            
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
            return result
            
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error processing video: {error_message}")
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            return {
                "error": error_message,
                "timestamp": timestamp
            }
    
    def analyze(self, video_path: str, output_path: Optional[str] = None, prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a video file and save the results to a JSON file.
        
        Args:
            video_path: Path to the video file
            output_path: Path to save the output JSON. If None, uses video_path + '.transcript.json'
            prompt: Optional prompt to guide the transcription
            
        Returns:
            The generated transcript data
            
        Raises:
            FileNotFoundError: If the video file doesn't exist
        """
        # Check if the file exists
        if not os.path.isfile(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Process the video
        result = self.process_video(video_path, prompt)
        
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
    
    parser = argparse.ArgumentParser(description="Video frame-based transcript analyzer")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("--output", "-o", help="Path to save the output JSON")
    parser.add_argument("--api-key", help="OpenAI API key (defaults to OPENAI_API_KEY env var)")
    parser.add_argument("--prompt", help="Optional prompt to guide transcription")
    
    args = parser.parse_args()
    
    try:
        analyzer = VideoAnalyzer(openai_api_key=args.api_key)
        analyzer.analyze(args.video_path, args.output, args.prompt)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
