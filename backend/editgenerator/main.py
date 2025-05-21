import os
import json
import logging
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

def process_transcript(transcript_data: Dict, user_brief: str) -> Dict:
    """Process transcript with AI to generate edited segments."""
    
    # Validate input data
    if not validate_json(transcript_data, INPUT_SCHEMA):
        return {"error": "Invalid input data format"}
    
    # Extract target duration from brief (assuming format like "~60 seconds")
    target_seconds = 60  # Default
    import re
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
        
        # Extract JSON from response
        response_text = response.content[0].text
        
        # Find JSON in the response
        import re
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(1))
        else:
            # Try to parse the entire response as JSON
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                return {"error": "Could not extract valid JSON from AI response", "response": response_text}
        
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
    
    except Exception as e:
        logger.error(f"Error processing transcript: {e}")
        return {"error": str(e)}

def main():
    """Main function to demonstrate functionality."""
    # This is a placeholder for demonstration
    print("AI-Editor module initialized. Import and use process_transcript() function to process transcripts.")

if __name__ == "__main__":
    main()
