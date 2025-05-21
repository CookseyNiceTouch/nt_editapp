import os
import json
import logging
import asyncio
import re
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from anthropic import Anthropic
import jsonschema

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
CLAUDE_API_KEY = os.getenv("claude_api_key")

# Constants
MODEL = "claude-3-7-sonnet-20250219"
MAX_TOKENS = 20000
THINKING_BUDGET = 16000

# Input and output schemas
INPUT_SCHEMA = {
    "type": "object",
    "required": ["file_name", "fps", "duration_frames", "speakers", "full_transcript", "words"],
    "properties": {
        "file_name": {"type": "string"},
        "fps": {"type": "number"},
        "duration_frames": {"type": "integer"},
        "speakers": {"type": "array", "items": {"type": "string"}},
        "full_transcript": {"type": "string"},
        "words": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["word", "speaker", "frame_in", "frame_out"],
                "properties": {
                    "word": {"type": "string"},
                    "speaker": {"type": "string"},
                    "frame_in": {"type": "integer", "minimum": 0},
                    "frame_out": {"type": "integer", "minimum": 0}
                }
            }
        }
    }
}

OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["file_name", "fps", "target_duration_frames", "actual_duration_frames", "segments"],
    "properties": {
        "file_name": {"type": "string"},
        "fps": {"type": "number"},
        "target_duration_frames": {"type": "integer"},
        "actual_duration_frames": {"type": "integer"},
        "segments": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["segment_id", "speaker", "frame_in", "frame_out", "text", "clip_order"],
                "properties": {
                    "segment_id": {"type": "integer"},
                    "speaker": {"type": "string"},
                    "frame_in": {"type": "integer", "minimum": 0},
                    "frame_out": {"type": "integer", "minimum": 0},
                    "text": {"type": "string"},
                    "clip_order": {"type": "integer", "minimum": 1}
                }
            }
        }
    }
}

def validate_json(data: Dict, schema: Dict) -> bool:
    """Validate JSON data against a schema."""
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"Validation error: {e}")
        return False

def create_system_prompt(transcript_data: Dict) -> str:
    """Create the system prompt for the AI model."""
    return f"""
    You are an expert video editor AI tasked with creating a rough cut from a video transcript.

    # TRANSCRIPT INFORMATION
    - File: {transcript_data['file_name']}
    - FPS: {transcript_data['fps']}
    - Duration: {transcript_data['duration_frames']} frames ({transcript_data['duration_frames'] / transcript_data['fps']:.2f} seconds)
    - Speakers: {', '.join(transcript_data['speakers'])}

    # YOUR TASK
    Based on the user's brief, you will select segments from the transcript to create a rough cut.
    You must follow these rules:
    1. Always prefer the last take for repeated phrases
    2. Omit silences (words with zero-length)
    3. Preserve approximate chronological order but allow reordering for narrative flow
    4. Interleave speakers if it serves the narrative

    # OUTPUT FORMAT
    You must output a JSON object with the following structure:
    ```
    {{
      "file_name": "{transcript_data['file_name']}",
      "fps": {transcript_data['fps']},
      "target_duration_frames": <calculated from brief>,
      "actual_duration_frames": <sum of segment lengths>,
      "segments": [
        {{
          "segment_id": 1,
          "speaker": "<speaker name>",
          "frame_in": <start frame>,
          "frame_out": <end frame>,
          "text": "<segment text>",
          "clip_order": 1
        }},
        // more segments...
      ]
    }}
    ```

    # CONSTRAINTS
    - Ensure frame_in < frame_out for all segments
    - Ensure frame_out <= {transcript_data['duration_frames']} for all segments
    - Segments should not overlap
    - The sum of segment durations should be close to the target duration specified in the brief
    """

def process_transcript_non_streaming(transcript_data: Dict, user_brief: str) -> Dict:
    """Process transcript with AI to generate edited segments using non-streaming API."""
    
    # Validate input data
    if not validate_json(transcript_data, INPUT_SCHEMA):
        return {"error": "Invalid input data format"}
    
    # Extract target duration from brief (assuming format like "~60 seconds")
    target_seconds = 60  # Default
    duration_match = re.search(r'~?(\d+)\s*seconds', user_brief)
    if duration_match:
        target_seconds = int(duration_match.group(1))
    
    # Calculate target frames
    target_frames = round(target_seconds * transcript_data["fps"])
    
    # Create system prompt
    system_prompt = create_system_prompt(transcript_data)
    
    # Initialize Anthropic client
    client = Anthropic(api_key=CLAUDE_API_KEY)
    
    try:
        # Call Claude with extended thinking
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            thinking={
                "type": "enabled",
                "budget_tokens": THINKING_BUDGET
            },
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Here is the transcript data:\n```json\n{json.dumps(transcript_data, indent=2)}\n```\n\nUser brief: {user_brief}\n\nPlease create an edited version based on this brief. Target duration: ~{target_seconds} seconds ({target_frames} frames)."
                }
            ]
        )
        
        # Find the text response
        response_text = None
        for block in response.content:
            if block.type == "text":
                response_text = block.text
                break
        
        if not response_text:
            return {"error": "No text content found in the response"}
        
        # Find JSON in the response
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(1))
        else:
            # Try to parse the entire response as JSON
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                return {"error": "Could not extract valid JSON from AI response", "response": response_text}
        
        return validate_and_process_result(result, transcript_data)
    
    except Exception as e:
        logger.error(f"Error processing transcript: {e}")
        return {"error": str(e)}

def process_transcript_stream(transcript_data: Dict, user_brief: str, show_thinking: bool = True) -> Dict:
    """Process transcript with AI to generate edited segments using streaming API."""
    
    # Validate input data
    if not validate_json(transcript_data, INPUT_SCHEMA):
        return {"error": "Invalid input data format"}
    
    # Extract target duration from brief (assuming format like "~60 seconds")
    target_seconds = 60  # Default
    duration_match = re.search(r'~?(\d+)\s*seconds', user_brief)
    if duration_match:
        target_seconds = int(duration_match.group(1))
    
    # Calculate target frames
    target_frames = round(target_seconds * transcript_data["fps"])
    
    # Create system prompt
    system_prompt = create_system_prompt(transcript_data)
    
    # Initialize Anthropic client
    client = Anthropic(api_key=CLAUDE_API_KEY)
    
    current_response = ""
    
    try:
        # Call Claude with extended thinking using streaming API
        if show_thinking:
            print("\n=== Claude's Thinking Process (streaming) ===")
            
        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            thinking={
                "type": "enabled",
                "budget_tokens": THINKING_BUDGET
            },
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Here is the transcript data:\n```json\n{json.dumps(transcript_data, indent=2)}\n```\n\nUser brief: {user_brief}\n\nPlease create an edited version based on this brief. Target duration: ~{target_seconds} seconds ({target_frames} frames)."
                }
            ]
        ) as stream:
            # Process the stream
            in_thinking_block = False
            in_text_block = False
            current_block_index = -1
            
            for event in stream:
                if event.type == "message_start":
                    if show_thinking:
                        print("Stream started")
                    
                elif event.type == "content_block_start":
                    current_block_index = event.index
                    block_type = event.content_block.type
                    
                    if block_type == "thinking":
                        in_thinking_block = True
                        if show_thinking:
                            print("\n--- Thinking started ---")
                    elif block_type == "text":
                        in_text_block = True
                        if show_thinking:
                            print("\n--- Response text ---")
                
                elif event.type == "content_block_delta":
                    if event.delta.type == "thinking_delta" and in_thinking_block and show_thinking:
                        print(event.delta.thinking, end="", flush=True)
                    elif event.delta.type == "text_delta" and in_text_block:
                        current_response += event.delta.text
                        if show_thinking:
                            print(event.delta.text, end="", flush=True)
                
                elif event.type == "content_block_stop":
                    if in_thinking_block and event.index == current_block_index:
                        in_thinking_block = False
                        if show_thinking:
                            print("\n--- Thinking complete ---")
                    elif in_text_block and event.index == current_block_index:
                        in_text_block = False
                        if show_thinking:
                            print("\n--- Response complete ---")
                
                elif event.type == "message_stop":
                    if show_thinking:
                        print("\n=== Stream completed ===")
        
        # Find JSON in the response
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', current_response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(1))
        else:
            # Try to parse the entire response as JSON
            try:
                result = json.loads(current_response)
            except json.JSONDecodeError:
                return {"error": "Could not extract valid JSON from AI response", "response": current_response}
        
        return validate_and_process_result(result, transcript_data)
    
    except Exception as e:
        logger.error(f"Error processing transcript with streaming: {e}")
        logger.debug(f"Partial response received: {current_response}")
        return {"error": f"Streaming error: {str(e)}"}

def validate_and_process_result(result, transcript_data):
    """Validate and process the result returned by Claude."""
    # Validate output
    if not validate_json(result, OUTPUT_SCHEMA):
        return {"error": "AI generated invalid output format", "response": result}
    
    # Perform additional validation
    for segment in result["segments"]:
        if segment["frame_out"] > transcript_data["duration_frames"]:
            return {"error": f"Segment {segment['segment_id']} has frame_out beyond video duration"}
        if segment["frame_in"] >= segment["frame_out"]:
            return {"error": f"Segment {segment['segment_id']} has invalid frame range"}
    
    # Check for overlapping segments when ordered by clip_order
    ordered_segments = sorted(result["segments"], key=lambda x: x["clip_order"])
    for i in range(1, len(ordered_segments)):
        if ordered_segments[i]["frame_in"] < ordered_segments[i-1]["frame_out"]:
            logger.warning(f"Segments {ordered_segments[i-1]['segment_id']} and {ordered_segments[i]['segment_id']} may overlap")
    
    # Check if actual duration is close to target
    tolerance = 0.1  # 10% tolerance
    if abs(result["actual_duration_frames"] - result["target_duration_frames"]) > result["target_duration_frames"] * tolerance:
        logger.warning(f"Actual duration ({result['actual_duration_frames']} frames) differs significantly from target ({result['target_duration_frames']} frames)")
    
    return result

def process_transcript(transcript_data: Dict, user_brief: str, show_thinking: bool = True, use_streaming: bool = True) -> Dict:
    """Process transcript with AI to generate edited segments."""
    
    if use_streaming:
        try:
            # Use the synchronous streaming function
            return process_transcript_stream(transcript_data, user_brief, show_thinking)
        except Exception as e:
            logger.error(f"Error in streaming processing: {e}")
            logger.info("Falling back to non-streaming API")
            return process_transcript_non_streaming(transcript_data, user_brief)
    else:
        # Use non-streaming API
        return process_transcript_non_streaming(transcript_data, user_brief)

def main():
    """Main function to demonstrate functionality."""
    import sys
    from pathlib import Path
    
    print("AI-Editor Module Demo")
    print("=====================")
    
    # Create a sample transcript for demonstration
    sample_transcript = {
        "file_name": "example.mp4",
        "fps": 30.0,
        "duration_frames": 3600,  # 2-minute video at 30fps
        "speakers": ["speaker1", "speaker2"],
        "full_transcript": "This is a sample transcript with multiple speakers. Speaker 1 talks about the main topic. Speaker 2 responds with additional information.",
        "words": [
            {"word": "This", "speaker": "speaker1", "frame_in": 30, "frame_out": 45},
            {"word": "is", "speaker": "speaker1", "frame_in": 46, "frame_out": 60},
            {"word": "a", "speaker": "speaker1", "frame_in": 61, "frame_out": 75},
            {"word": "sample", "speaker": "speaker1", "frame_in": 76, "frame_out": 90},
            {"word": "transcript", "speaker": "speaker1", "frame_in": 91, "frame_out": 120},
            {"word": "with", "speaker": "speaker1", "frame_in": 121, "frame_out": 135},
            {"word": "multiple", "speaker": "speaker1", "frame_in": 136, "frame_out": 165},
            {"word": "speakers", "speaker": "speaker1", "frame_in": 166, "frame_out": 195},
            {"word": "Speaker", "speaker": "speaker2", "frame_in": 300, "frame_out": 330},
            {"word": "1", "speaker": "speaker2", "frame_in": 331, "frame_out": 345},
            {"word": "talks", "speaker": "speaker2", "frame_in": 346, "frame_out": 375},
            {"word": "about", "speaker": "speaker2", "frame_in": 376, "frame_out": 405},
            {"word": "the", "speaker": "speaker2", "frame_in": 406, "frame_out": 420},
            {"word": "main", "speaker": "speaker2", "frame_in": 421, "frame_out": 450},
            {"word": "topic", "speaker": "speaker2", "frame_in": 451, "frame_out": 480},
            {"word": "Speaker", "speaker": "speaker1", "frame_in": 600, "frame_out": 630},
            {"word": "2", "speaker": "speaker1", "frame_in": 631, "frame_out": 645},
            {"word": "responds", "speaker": "speaker1", "frame_in": 646, "frame_out": 690},
            {"word": "with", "speaker": "speaker1", "frame_in": 691, "frame_out": 720},
            {"word": "additional", "speaker": "speaker1", "frame_in": 721, "frame_out": 765},
            {"word": "information", "speaker": "speaker1", "frame_in": 766, "frame_out": 810}
        ]
    }
    
    # Check if a transcript file was provided
    transcript_data = sample_transcript
    if len(sys.argv) > 1:
        transcript_path = Path(sys.argv[1])
        if transcript_path.exists():
            print(f"Loading transcript from {transcript_path}")
            try:
                with open(transcript_path, 'r') as f:
                    transcript_data = json.load(f)
            except Exception as e:
                print(f"Error loading transcript file: {e}")
                print("Using sample transcript instead.")
        else:
            print(f"File {transcript_path} not found. Using sample transcript instead.")
    else:
        print("No transcript file provided. Using sample transcript.")
    
    # Get user brief
    if len(sys.argv) > 2:
        user_brief = sys.argv[2]
    else:
        user_brief = "Create a ~30 seconds highlight focusing on key points about the main topic."
        print(f"No user brief provided. Using default: '{user_brief}'")
    
    # Get streaming option
    use_streaming = True
    if len(sys.argv) > 3:
        if sys.argv[3].lower() in ["false", "no", "0"]:
            use_streaming = False
            print("Streaming disabled")
    
    # Process the transcript
    print("\nProcessing transcript...")
    result = process_transcript(transcript_data, user_brief, show_thinking=True, use_streaming=use_streaming)
    
    # Print the result
    print("\nResult:")
    print(json.dumps(result, indent=2))
    
    # Save the result to a file
    output_path = Path("edited_output.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nOutput saved to {output_path.absolute()}")

if __name__ == "__main__":
    main()
