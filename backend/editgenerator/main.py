import os
import json
import logging
import re
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
import jsonschema

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Store command-line args globally
args = None

# Load environment variables
load_dotenv()
CLAUDE_API_KEY = os.getenv("claude_api_key")

# Constants
MODEL = "claude-3-7-sonnet-20250219"
MAX_TOKENS = 20000
THINKING_BUDGET = 16000

# Paths
CURRENT_DIR = Path(__file__).parent
PROMPTS_DIR = CURRENT_DIR / "prompts"
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "systempromptv1.md"
USER_PROMPT_PATH = PROMPTS_DIR / "userpromptv1.md"
PROJECT_BRIEF_PATH = PROMPTS_DIR / "projectbrieftemp.md"
EDITS_DIR = CURRENT_DIR / "edits"

# Ensure edits directory exists
EDITS_DIR.mkdir(exist_ok=True)

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
    """Load content from a file with proper encoding handling."""
    try:
        # First try UTF-8 encoding (most common for text files with special characters)
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # If UTF-8 fails, try with utf-8-sig (handles BOM)
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                return f.read()
        except UnicodeDecodeError:
            # Last resort, try with system default encoding but ignore errors
            try:
                with open(file_path, 'r', encoding='cp1252', errors='replace') as f:
                    content = f.read()
                    logger.warning(f"File {file_path} had to be read with fallback encoding, some characters may be replaced")
                    return content
            except Exception as e:
                logger.error(f"Failed to load file {file_path} with any encoding: {e}")
                raise
    except Exception as e:
        logger.error(f"Error loading file {file_path}: {e}")
        raise

def load_system_prompt(prompt_path: Path = SYSTEM_PROMPT_PATH) -> str:
    """Load system prompt from file."""
    try:
        content = load_file_content(prompt_path)
        logger.info(f"Successfully loaded system prompt ({len(content)} chars)")
        return content
    except Exception as e:
        logger.error(f"Error loading system prompt: {e}")
        raise RuntimeError(f"Failed to load system prompt from {prompt_path}: {e}")

def load_user_prompt(prompt_path: Path = USER_PROMPT_PATH) -> str:
    """Load user prompt from file."""
    try:
        content = load_file_content(prompt_path)
        logger.info(f"Successfully loaded user prompt ({len(content)} chars)")
        return content
    except Exception as e:
        logger.error(f"Error loading user prompt: {e}")
        raise RuntimeError(f"Failed to load user prompt from {prompt_path}: {e}")

def load_project_brief() -> str:
    """Load the project brief content."""
    if not PROJECT_BRIEF_PATH.exists():
        logger.error(f"Project brief file not found at {PROJECT_BRIEF_PATH}")
        raise FileNotFoundError(f"Project brief file not found at {PROJECT_BRIEF_PATH}")
    
    try:
        content = load_file_content(PROJECT_BRIEF_PATH)
        logger.info(f"Successfully loaded project brief ({len(content)} chars)")
        return content
    except Exception as e:
        logger.error(f"Error loading project brief: {e}")
        raise RuntimeError(f"Failed to load project brief from {PROJECT_BRIEF_PATH}: {e}")

def verify_files():
    """Verify that all necessary files can be loaded correctly."""
    files_ok = True
    errors = []
    
    print("\nVerifying prompt files...")
    
    # Check if system prompt file exists and can be loaded
    if not SYSTEM_PROMPT_PATH.exists():
        print(f"❌ System prompt file not found: {SYSTEM_PROMPT_PATH}")
        files_ok = False
        errors.append(f"Missing system prompt file: {SYSTEM_PROMPT_PATH}")
    else:
        try:
            content = load_file_content(SYSTEM_PROMPT_PATH)
            print(f"✅ System prompt file verified: {SYSTEM_PROMPT_PATH} ({len(content)} chars)")
        except Exception as e:
            print(f"❌ Could not read system prompt file: {e}")
            files_ok = False
            errors.append(f"Error reading system prompt: {e}")
    
    # Check if user prompt file exists and can be loaded
    if not USER_PROMPT_PATH.exists():
        print(f"❌ User prompt file not found: {USER_PROMPT_PATH}")
        files_ok = False
        errors.append(f"Missing user prompt file: {USER_PROMPT_PATH}")
    else:
        try:
            content = load_file_content(USER_PROMPT_PATH)
            print(f"✅ User prompt file verified: {USER_PROMPT_PATH} ({len(content)} chars)")
        except Exception as e:
            print(f"❌ Could not read user prompt file: {e}")
            files_ok = False
            errors.append(f"Error reading user prompt: {e}")
            
    # Check if project brief file exists and can be loaded
    if not PROJECT_BRIEF_PATH.exists():
        print(f"❌ Project brief file not found: {PROJECT_BRIEF_PATH}")
        files_ok = False
        errors.append(f"Missing project brief file: {PROJECT_BRIEF_PATH}")
    else:
        try:
            content = load_file_content(PROJECT_BRIEF_PATH)
            print(f"✅ Project brief file verified: {PROJECT_BRIEF_PATH} ({len(content)} chars)")
        except Exception as e:
            print(f"❌ Could not read project brief file: {e}")
            files_ok = False
            errors.append(f"Error reading project brief: {e}")
    
    if not files_ok:
        print("\n❌ Some required files could not be verified.")
        print("   Errors:")
        for error in errors:
            print(f"   - {error}")
        print("\nPlease fix these issues before continuing.")
        raise RuntimeError("Required prompt files are missing or cannot be read")
    else:
        print("\n✅ All prompt files verified successfully.")
    
    return files_ok

def create_system_prompt(transcript_data: Dict) -> str:
    """Create the system prompt for the AI model by formatting the template."""
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
    
    return formatted_prompt

def create_user_prompt(transcript_data: Dict, user_brief: Optional[str], target_seconds: int, target_frames: int) -> str:
    """Create the user prompt by formatting the template with transcript data and user brief."""
    # Load the user prompt template
    prompt_template = load_user_prompt()
    
    # Load the project brief content
    project_brief = load_project_brief()
    
    # Create brief section with both user brief and project brief
    combined_brief = ""
    if user_brief:
        combined_brief += f"USER BRIEF: {user_brief}\n\n"
    
    combined_brief += f"PROJECT BRIEF:\n{project_brief}\n\n"
    
    # Format the template with transcript data and combined briefs
    formatted_prompt = prompt_template.format(
        transcript_json=json.dumps(transcript_data, indent=2),
        user_brief=combined_brief,
        target_seconds=target_seconds,
        target_frames=target_frames
    )
    
    return formatted_prompt

def extract_duration_from_brief() -> int:
    """Extract target duration from project brief."""
    project_brief = load_project_brief()
    
    # Look for 'Length: X–Y minutes' format
    minutes_match = re.search(r'Length:\s*([\d.]+)[–-]([\d.]+)\s*minutes', project_brief)
    if minutes_match:
        # Use the average of the range
        min_minutes = float(minutes_match.group(1))
        max_minutes = float(minutes_match.group(2))
        avg_minutes = (min_minutes + max_minutes) / 2
        seconds = int(avg_minutes * 60)
        logger.info(f"Duration extracted from project brief: {min_minutes}-{max_minutes} minutes = {seconds} seconds")
        return seconds
    
    # If no explicit duration found, raise an error
    logger.error("No duration specification found in project brief")
    raise ValueError("Could not extract duration from project brief. Format should be 'Length: X-Y minutes'")

def process_transcript_stream(transcript_data: Dict, user_brief: Optional[str], show_thinking: bool = True) -> Dict:
    """Process transcript with AI to generate edited segments using streaming API."""
    
    # Validate input data
    if not validate_json(transcript_data, INPUT_SCHEMA):
        return {"error": "Invalid input data format"}
    
    # Get target duration from project brief
    target_seconds = extract_duration_from_brief()
    
    # If user specified a duration in their brief, override the project brief duration
    if user_brief:
        duration_match = re.search(r'~?(\d+)\s*seconds', user_brief)
        if duration_match:
            user_seconds = int(duration_match.group(1))
            logger.info(f"Overriding project brief duration with user-specified duration: {user_seconds} seconds")
            target_seconds = user_seconds
    
    # Calculate target frames
    target_frames = round(target_seconds * transcript_data["fps"])
    logger.info(f"Target duration: {target_seconds} seconds = {target_frames} frames at {transcript_data['fps']} fps")
    
    # Create system prompt
    system_prompt = create_system_prompt(transcript_data)
    if args and args.debug:
        print(f"System prompt length: {len(system_prompt)} chars")
        print(f"System prompt first 100 chars: {system_prompt[:100]}...")
    
    # Create user prompt with project brief included directly
    user_prompt = create_user_prompt(transcript_data, user_brief, target_seconds, target_frames)
    if args and args.debug:
        print(f"User prompt length: {len(user_prompt)} chars")
        print(f"User prompt first 100 chars: {user_prompt[:100]}...")
    
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
                    "content": user_prompt
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
            try:
                result = json.loads(json_match.group(1))
            except json.JSONDecodeError as e:
                return {"error": f"Found code block but couldn't parse as JSON: {e}", "response": json_match.group(1)}
        else:
            # Try to parse the entire response as JSON
            try:
                result = json.loads(current_response)
            except json.JSONDecodeError:
                # If that fails, try to convert markdown format to JSON
                try:
                    result = convert_markdown_to_json(current_response, transcript_data, target_frames)
                except Exception as e:
                    return {"error": "Could not extract valid JSON from AI response", "response": current_response}
        
        return validate_and_process_result(result, transcript_data)
    
    except Exception as e:
        logger.error(f"Error processing transcript with streaming: {e}")
        logger.debug(f"Partial response received: {current_response}")
        return {"error": f"Streaming error: {str(e)}"}

def convert_markdown_to_json(markdown_text: str, transcript_data: Dict, target_frames: int) -> Dict:
    """Convert markdown format to the expected JSON format."""
    logger.info("Attempting to convert markdown response to JSON")
    
    # Initialize the result structure
    result = {
        "file_name": transcript_data["file_name"],
        "fps": transcript_data["fps"],
        "target_duration_frames": target_frames,
        "actual_duration_frames": 0,
        "segments": []
    }
    
    # Extract clip info from markdown
    clip_pattern = r'## CLIP (\d+).*?(\d{2}:\d{2}:\d{2}\.\d{2}) - (\d{2}:\d{2}:\d{2}\.\d{2}).*?```\n(.*?)```'
    clips = re.findall(clip_pattern, markdown_text, re.DOTALL)
    
    if not clips:
        raise ValueError("Could not extract clips from markdown format")
    
    total_duration = 0
    for i, (clip_num, time_in, time_out, text) in enumerate(clips, 1):
        # Parse the timestamp into frames
        frame_in = timestamp_to_frames(time_in, transcript_data["fps"])
        frame_out = timestamp_to_frames(time_out, transcript_data["fps"])
        
        # Extract speakers and text
        lines = text.strip().split('\n')
        segment_text = text.strip()
        speaker = None
        
        # Determine speaker - try to extract from format like "[Cooksey] Hi, I'm Cooksey."
        speaker_match = re.match(r'\[(.*?)\]', lines[0])
        if speaker_match:
            speaker = speaker_match.group(1)
        else:
            # Find the closest speaker based on the frame range
            speaker = find_speaker_for_segment(transcript_data, frame_in, frame_out)
        
        # Add segment to the result
        segment = {
            "segment_id": i,
            "speaker": speaker,
            "frame_in": frame_in,
            "frame_out": frame_out,
            "text": segment_text,
            "clip_order": i
        }
        
        result["segments"].append(segment)
        total_duration += (frame_out - frame_in)
    
    result["actual_duration_frames"] = total_duration
    return result

def timestamp_to_frames(timestamp: str, fps: float) -> int:
    """Convert a timestamp (HH:MM:SS.FF) to frame number."""
    hours, minutes, seconds_ms = timestamp.split(':')
    seconds, ms = seconds_ms.split('.')
    
    total_seconds = (int(hours) * 3600) + (int(minutes) * 60) + int(seconds)
    total_frames = int(total_seconds * fps)
    
    # Add frames from milliseconds (assuming ms is actually frames for simplicity)
    if len(ms) == 2:  # If it's actually a frame number in the time format
        total_frames += int(ms)
    else:  # If it's milliseconds
        ms_frames = int(float(f"0.{ms}") * fps)
        total_frames += ms_frames
    
    return total_frames

def find_speaker_for_segment(transcript_data: Dict, frame_in: int, frame_out: int) -> str:
    """Find the most likely speaker for a segment based on the transcript."""
    speaker_counts = {}
    
    for word in transcript_data["words"]:
        if frame_in <= word["frame_in"] <= frame_out or frame_in <= word["frame_out"] <= frame_out:
            speaker = word["speaker"]
            speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1
    
    if speaker_counts:
        # Return the speaker with the most words in this segment
        return max(speaker_counts.items(), key=lambda x: x[1])[0]
    else:
        # Fallback to the first speaker if no words found in the range
        return transcript_data["speakers"][0] if transcript_data["speakers"] else "Unknown"

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

def process_transcript(transcript_data: Dict, user_brief: Optional[str], show_thinking: bool = True) -> Dict:
    """Process transcript with AI to generate edited segments."""
    return process_transcript_stream(transcript_data, user_brief, show_thinking)

def main():
    """Main function to demonstrate functionality."""
    import sys
    from pathlib import Path
    import argparse
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='AI-Editor: Generate edited segments from video transcripts')
    parser.add_argument('transcript_file', type=str, help='Path to the transcript JSON file')
    parser.add_argument('--brief', '-b', type=str, 
                        help='Optional user brief to supplement the project brief')
    parser.add_argument('--output', '-o', type=str,
                        help='Custom output filename')
    parser.add_argument('--debug', '-d', action='store_true',
                        help='Enable debug mode with verbose logging')
    parser.add_argument('--dump-prompts', action='store_true',
                        help='Dump system and user prompts to files for debugging')
    parser.add_argument('--verify', '-v', action='store_true',
                        help='Verify prompt files and exit')
    
    # Parse arguments
    global args
    args = parser.parse_args()
    
    # Set more verbose logging if debug is enabled
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    
    print("AI-Editor Module")
    print("===============")
    
    # Verify files if requested
    if args.verify:
        verify_files()
        return 0
    
    # Always run a quick verification
    verify_files()
    
    # Check if transcript file exists
    transcript_path = Path(args.transcript_file)
    if not transcript_path.exists():
        print(f"Error: File {transcript_path} not found")
        return 1
    
    print(f"Loading transcript from {transcript_path}")
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_data = json.load(f)
    except UnicodeDecodeError:
        try:
            with open(transcript_path, 'r', encoding='utf-8-sig') as f:
                transcript_data = json.load(f)
        except Exception as e:
            print(f"Error loading transcript file with UTF-8 or UTF-8-SIG encoding: {e}")
            print("Trying with system default encoding...")
            try:
                with open(transcript_path, 'r') as f:
                    transcript_data = json.load(f)
            except Exception as e:
                print(f"Error loading transcript file: {e}")
                return 1
    except Exception as e:
        print(f"Error loading transcript file: {e}")
        return 1
    
    # Check if project brief exists
    if PROJECT_BRIEF_PATH.exists():
        print(f"Using project brief: {PROJECT_BRIEF_PATH}")
        if args.debug:
            try:
                brief_content = load_file_content(PROJECT_BRIEF_PATH)
                print("\nProject Brief Content:")
                print("-" * 40)
                print(brief_content[:500] + ("..." if len(brief_content) > 500 else ""))
                print("-" * 40)
                
                # Extract duration from brief for debugging
                minutes_match = re.search(r'Length:\s*([\d.]+)[–-]([\d.]+)\s*minutes', brief_content)
                if minutes_match:
                    min_minutes = float(minutes_match.group(1))
                    max_minutes = float(minutes_match.group(2))
                    avg_minutes = (min_minutes + max_minutes) / 2
                    print(f"Duration found in brief: {min_minutes}-{max_minutes} minutes (avg: {avg_minutes} min = {int(avg_minutes * 60)} sec)")
            except Exception as e:
                print(f"Error reading project brief: {e}")
    else:
        print(f"WARNING: Project brief not found at {PROJECT_BRIEF_PATH}")
        print("The edit will be created without proper project specifications.")
    
    # Process the transcript
    print("\nProcessing transcript...")
    
    # Save intermediate data for debugging if requested
    if args.dump_prompts:
        try:
            # Use the duration from project brief
            target_seconds = extract_duration_from_brief()
            target_frames = round(target_seconds * transcript_data["fps"])
            
            system_prompt = create_system_prompt(transcript_data)
            user_prompt = create_user_prompt(transcript_data, args.brief, target_seconds, target_frames)
            
            # Write prompts to files
            debug_dir = CURRENT_DIR / "debug"
            debug_dir.mkdir(exist_ok=True)
            
            with open(debug_dir / "system_prompt_debug.md", 'w', encoding='utf-8') as f:
                f.write(system_prompt)
            print(f"Saved system prompt to {debug_dir / 'system_prompt_debug.md'}")
            
            with open(debug_dir / "user_prompt_debug.md", 'w', encoding='utf-8') as f:
                f.write(user_prompt)
            print(f"Saved user prompt to {debug_dir / 'user_prompt_debug.md'}")
            
        except Exception as e:
            print(f"Error in debug prompt saving: {e}")
    
    result = process_transcript(
        transcript_data, 
        args.brief, 
        show_thinking=True
    )
    
    # Print the result
    print("\nResult:")
    print(json.dumps(result, indent=2))
    
    # Save the result to a file
    if args.output:
        output_path = Path(args.output)
    else:
        # Save to the edits directory with a fixed filename
        output_path = EDITS_DIR / "edited_output.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    print(f"\nOutput saved to {output_path.absolute()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
