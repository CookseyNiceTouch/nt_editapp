import os
import json
import logging
import asyncio
from pathlib import Path
import time
from typing import Dict, Any, Optional, Tuple
from dotenv import load_dotenv
import anthropic
from anthropic import Anthropic
from jsonschema import validate
from prompts.prompts import system_prompt, user_prompt

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Constants
CLAUDE_MODEL = "claude-3-7-sonnet-20250219"
MAX_TOKENS = 20000
THINKING_BUDGET = 16000  # Maximum tokens for Claude's extended thinking process
TARGET_SCHEMA = {
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
                    "frame_in": {"type": "integer"},
                    "frame_out": {"type": "integer"},
                    "text": {"type": "string"},
                    "clip_order": {"type": "integer"}
                }
            }
        }
    }
}

def load_prompts(transcript_data: Dict[str, Any], user_brief: str) -> Tuple[str, str]:
    """Load system prompt and format user prompt with transcript data and brief."""
    system = system_prompt()
    transcript_json = json.dumps(transcript_data, indent=2)
    user = user_prompt(transcript_json=transcript_json, brief=user_brief)
    return system, user

async def process_transcript_async(
    transcript_data: Dict[str, Any], 
    user_brief: str,
    output_filename: Optional[str] = None,
    streaming_callback: Optional[callable] = None
) -> Dict[str, Any]:
    """Process a transcript using Claude API with streaming and thinking features."""
    logger.info("Starting transcript processing")
    
    try:
        # Initialize Claude client
        api_key = os.environ.get("claude_api_key")
        if not api_key:
            raise ValueError("Claude API key not found. Set claude_api_key in .env file.")
        
        client = Anthropic(api_key=api_key)
        
        # Get prompts
        system_prompt, user_prompt = load_prompts(transcript_data, user_brief)
        
        # Create a message with streaming
        logger.info("Sending request to Claude API with thinking enabled")
        
        # Process with streaming
        thinking_content = ""
        response_content = ""
        
        # Create completion with proper streaming handling
        with client.messages.stream(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            thinking={"type": "enabled", "budget_tokens": THINKING_BUDGET},
        ) as stream:
            # Process the stream events
            for event in stream:
                if hasattr(event, 'type') and event.type == "content_block_delta":
                    if hasattr(event, 'delta'):
                        if event.delta.type == "thinking_delta":
                            thinking_content += event.delta.thinking
                            if streaming_callback:
                                streaming_callback("thinking", event.delta.thinking)
                        elif event.delta.type == "text_delta":
                            response_content += event.delta.text
                            if streaming_callback:
                                streaming_callback("response", event.delta.text)
        
        # Save thinking output for debugging if needed
        if output_filename:
            thinking_path = Path(output_filename).with_suffix(".thinking.txt")
            with open(thinking_path, "w") as f:
                f.write(thinking_content)
            
        # Parse the JSON response
        try:
            logger.info("Parsing Claude's response as JSON")
            result = json.loads(response_content)
            
            # Validate against schema
            validate(instance=result, schema=TARGET_SCHEMA)
            
            # Save to file if output_filename is specified
            if output_filename:
                with open(output_filename, "w") as f:
                    json.dump(result, f, indent=2)
            
            return result
        
        except json.JSONDecodeError:
            error_msg = f"Failed to parse Claude's response as JSON. Raw response: {response_content[:500]}..."
            logger.error(error_msg)
            return {"error": "JSON parsing error", "details": error_msg}
        
        except Exception as e:
            logger.error(f"Error validating or processing result: {str(e)}")
            return {"error": str(e)}
    
    except Exception as e:
        logger.error(f"Error processing transcript: {str(e)}")
        return {"error": str(e)}

def process_transcript(
    transcript_data: Dict[str, Any], 
    user_brief: str,
    output_filename: Optional[str] = None,
    streaming_callback: Optional[callable] = None
) -> Dict[str, Any]:
    """Synchronous wrapper around the async process_transcript function."""
    
    # Get the current event loop or create a new one
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(
        process_transcript_async(
            transcript_data, 
            user_brief,
            output_filename, 
            streaming_callback
        )
    )

def stream_to_console(stream_type: str, content: str):
    """
    Improved streaming callback that prints to console in a more readable format.
    Buffers content and prints in a cleaner way.
    """
    if stream_type == "thinking":
        # For thinking content, print in gray
        # Only print complete sentences or reasonable chunks
        if content.endswith(('.', '!', '?', '\n')) or len(content) > 80:
            print(f"\033[90mThinking: {content}\033[0m")
        else:
            # For small fragments, print without newline
            print(f"\033[90m{content}\033[0m", end="")
    else:
        # For response content (JSON), print in green
        # Only print complete JSON elements or reasonable chunks
        if content.endswith(('}', ']', ',')) or len(content) > 80:
            print(f"\033[92m{content}\033[0m")
        else:
            # For small fragments, print without newline
            print(f"\033[92m{content}\033[0m", end="")

# Main execution when script is run directly
if __name__ == "__main__":
    import sys
    
    # Check if transcript file path is provided as argument
    if len(sys.argv) < 2:
        print("Usage: python main.py <transcript_file.json> [brief]")
        sys.exit(1)
    
    # Get transcript path from command line
    transcript_path = sys.argv[1]
    
    # Use default brief or get from command line
    if len(sys.argv) > 2:
        user_brief = sys.argv[2]
    else:
        # Use the content of projectbrieftemp.txt as default brief
        brief_path = Path(__file__).parent / "prompts" / "projectbrieftemp.txt"
        with open(brief_path, "r", encoding="utf-8") as f:
            user_brief = f.read()
    
    # Load transcript data
    with open(transcript_path, "r") as f:
        transcript_data = json.load(f)
    
    # Set output path to edits folder
    output_dir = Path(__file__).parent / "edits"
    output_dir.mkdir(exist_ok=True)
    
    output_filename = output_dir / f"{Path(transcript_path).stem}.edited.json"
    
    print(f"Processing transcript: {transcript_path}")
    print(f"Using brief: {user_brief[:100]}...")  # Show first 100 chars
    print(f"Output will be saved to: {output_filename}")
    print("\nStarting Claude processing with thinking enabled...\n")
    
    # Process with streaming to console
    result = process_transcript(
        transcript_data, 
        user_brief, 
        output_filename=str(output_filename),
        streaming_callback=stream_to_console
    )
    
    print("\n\nProcessing complete.")
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Generated {len(result['segments'])} segments")
        print(f"Target duration: {result['target_duration_frames']} frames")
        print(f"Actual duration: {result['actual_duration_frames']} frames")
