import os
import json
import logging
import asyncio
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
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

# Paths
CURRENT_DIR = Path(__file__).parent
SYSTEM_PROMPT_PATH = CURRENT_DIR / "systempromptv1.md"

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

def load_file_content(file_path: Path) -> str:
    """Load content from a file."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading file {file_path}: {e}")
        raise

def load_system_prompt(prompt_path: Path = SYSTEM_PROMPT_PATH) -> str:
    """Load system prompt from file."""
    return load_file_content(prompt_path)

def load_external_context(context_path: Path) -> str:
    """Load external context document."""
    return load_file_content(context_path)

def create_system_prompt(transcript_data: Dict, context_files: List[Path] = None) -> str:
    """Create the system prompt for the AI model by formatting the template and adding context."""
    try:
        # Load the system prompt template
        prompt_template = load_system_prompt()
        
        # Format the template with transcript data
        duration_seconds = transcript_data['duration_frames'] / transcript_data['fps']
        formatted_prompt = prompt_template.format(
            file_name=transcript_data['file_name'],
            fps=transcript_data['fps'],
            duration_frames=transcript_data['duration_frames'],
            duration_seconds=duration_seconds,
            speakers=", ".join(transcript_data['speakers'])
        )
        
        # Add external context if provided
        if context_files and len(context_files) > 0:
            formatted_prompt += "\n\n# ADDITIONAL CONTEXT\n"
            for i, context_path in enumerate(context_files):
                try:
                    context_content = load_external_context(context_path)
                    context_name = context_path.stem
                    formatted_prompt += f"\n## {context_name.upper()}\n{context_content}\n"
                except Exception as e:
                    logger.warning(f"Could not load context file {context_path}: {e}")
        
        return formatted_prompt
    except Exception as e:
        logger.error(f"Error creating system prompt: {e}")
        # Fallback to a basic prompt if there's an error
        return f"You are an expert video editor. Create a rough cut from the transcript of {transcript_data['file_name']}."

def process_transcript_non_streaming(transcript_data: Dict, user_brief: str, context_files: List[Path] = None) -> Dict:
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
    
    # Create system prompt with context
    system_prompt = create_system_prompt(transcript_data, context_files)
    
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

def process_transcript_stream(transcript_data: Dict, user_brief: str, context_files: List[Path] = None, show_thinking: bool = True) -> Dict:
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
    
    # Create system prompt with context
    system_prompt = create_system_prompt(transcript_data, context_files)
    
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

def process_transcript(transcript_data: Dict, user_brief: str, context_files: List[Path] = None, show_thinking: bool = True, use_streaming: bool = True) -> Dict:
    """Process transcript with AI to generate edited segments."""
    
    if use_streaming:
        try:
            # Use the synchronous streaming function
            return process_transcript_stream(transcript_data, user_brief, context_files, show_thinking)
        except Exception as e:
            logger.error(f"Error in streaming processing: {e}")
            logger.info("Falling back to non-streaming API")
            return process_transcript_non_streaming(transcript_data, user_brief, context_files)
    else:
        # Use non-streaming API
        return process_transcript_non_streaming(transcript_data, user_brief, context_files)

def main():
    """Main function to demonstrate functionality."""
    import sys
    from pathlib import Path
    import argparse
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='AI-Editor: Generate edited segments from video transcripts')
    parser.add_argument('transcript_file', type=str, help='Path to the transcript JSON file')
    parser.add_argument('--brief', '-b', type=str, default="Create a ~30 seconds highlight focusing on key points", 
                        help='User brief describing the desired edit')
    parser.add_argument('--context', '-c', type=str, nargs='+', 
                        help='Additional context files (e.g., project briefs)')
    parser.add_argument('--no-stream', action='store_true', 
                        help='Disable streaming (use regular API calls)')
    parser.add_argument('--output', '-o', type=str,
                        help='Custom output filename')
    
    args = parser.parse_args()
    
    print("AI-Editor Module")
    print("===============")
    
    # Check if transcript file exists
    transcript_path = Path(args.transcript_file)
    if not transcript_path.exists():
        print(f"Error: File {transcript_path} not found")
        return 1
    
    print(f"Loading transcript from {transcript_path}")
    try:
        with open(transcript_path, 'r') as f:
            transcript_data = json.load(f)
    except Exception as e:
        print(f"Error loading transcript file: {e}")
        return 1
    
    # Process context files if provided
    context_files = []
    if args.context:
        for context_path_str in args.context:
            context_path = Path(context_path_str)
            if context_path.exists():
                context_files.append(context_path)
                print(f"Added context file: {context_path}")
            else:
                print(f"Warning: Context file not found: {context_path}")
    
    # Get streaming option
    use_streaming = not args.no_stream
    if not use_streaming:
        print("Streaming disabled")
    
    # Process the transcript
    print("\nProcessing transcript...")
    result = process_transcript(
        transcript_data, 
        args.brief, 
        context_files=context_files,
        show_thinking=True, 
        use_streaming=use_streaming
    )
    
    # Print the result
    print("\nResult:")
    print(json.dumps(result, indent=2))
    
    # Save the result to a file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = transcript_path.with_suffix('.edited.json')
    
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\nOutput saved to {output_path.absolute()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
