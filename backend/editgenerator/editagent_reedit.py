import os
import json
import logging
import asyncio
from pathlib import Path
import time
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import glob
from dotenv import load_dotenv
import anthropic
from anthropic import Anthropic
from jsonschema import validate
from prompts.prompts_reedit import system_prompt, user_prompt

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get paths relative to script location (backend/editgenerator)
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # Go up from backend/editgenerator to project root

# File paths (relative to project root)
ANALYZED_DIR = PROJECT_ROOT / "data" / "analyzed"
PROJECT_DATA_PATH = PROJECT_ROOT / "data" / "projectdata.json"
TIMELINE_EDITED_DIR = PROJECT_ROOT / "data" / "timelineprocessing" / "timeline_edited"
TIMELINE_REF_DIR = PROJECT_ROOT / "data" / "timelineprocessing" / "timeline_ref"

# Will be loaded from project data
project_name = None
project_brief = None

# Constants
CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 20000
THINKING_BUDGET = 16000  # Maximum tokens for Claude's extended thinking process

TARGET_SCHEMA = {
    "type": "object",
    "required": ["schema_version", "otio_schema_version", "timeline", "tracks", "summary"],
    "properties": {
        "schema_version": {"type": "string"},
        "otio_schema_version": {"type": "string"},
        "timeline": {
            "type": "object",
            "required": ["name", "fps", "metadata"],
            "properties": {
                "name": {"type": "string"},
                "fps": {"type": "number"},
                "metadata": {"type": "object"}
            }
        },
        "tracks": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["track_index", "name", "kind", "clips", "metadata"],
                "properties": {
                    "track_index": {"type": "integer"},
                    "name": {"type": "string"},
                    "kind": {"type": "string"},
                    "clips": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["clip_index", "name", "metadata", "source_range", "media_reference"],
                            "properties": {
                                "clip_index": {"type": "integer"},
                                "name": {"type": "string"},
                                "metadata": {"type": "object"},
                                "source_range": {"type": "object"},
                                "media_reference": {"type": "object"}
                            }
                        }
                    },
                    "metadata": {"type": "object"}
                }
            }
        },
        "summary": {
            "type": "object",
            "required": ["total_tracks", "total_clips", "timeline_duration_frames"],
            "properties": {
                "total_tracks": {"type": "integer"},
                "total_clips": {"type": "integer"},
                "timeline_duration_frames": {"type": "integer"}
            }
        }
    }
}

def find_existing_timeline_json() -> Optional[Path]:
    """Find existing JSON file in timeline_edited directory to use as input."""
    try:
        # Look for JSON files in timeline_edited directory
        json_files = list(TIMELINE_EDITED_DIR.glob("*.json"))
        
        if json_files:
            if len(json_files) > 1:
                logger.warning(f"Multiple JSON files found in {TIMELINE_EDITED_DIR}:")
                for f in json_files:
                    logger.warning(f"  - {f.name}")
                logger.warning("Using the first one found...")
            
            existing_json = json_files[0]
            logger.info(f"Found existing timeline JSON: {existing_json.name}")
            return existing_json
        else:
            logger.info(f"No existing JSON files found in {TIMELINE_EDITED_DIR}")
            return None
            
    except Exception as e:
        logger.warning(f"Error checking for existing JSON files: {e}")
        return None

def generate_reedit_filename(project_title: str, iteration: int = None) -> Path:
    """Generate output filename for re-edited timeline."""
    
    # Ensure output directory exists
    TIMELINE_EDITED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Clean project title for filename (remove invalid characters)
    clean_title = "".join(c for c in project_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_title = clean_title.replace(' ', '_')
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create filename with iteration marker
    if iteration:
        filename = f"{clean_title}_reedit_v{iteration}_{timestamp}.json"
    else:
        filename = f"{clean_title}_reedit_{timestamp}.json"
    
    output_path = TIMELINE_EDITED_DIR / filename
    
    logger.info(f"Generated reedit filename: {filename}")
    return output_path

def load_project_data() -> Dict[str, str]:
    """Load project data from the standard project data file."""
    global project_name, project_brief
    
    if not PROJECT_DATA_PATH.exists():
        raise FileNotFoundError(f"Project data file not found at: {PROJECT_DATA_PATH}")
    
    try:
        with open(PROJECT_DATA_PATH, "r", encoding="utf-8") as f:
            project_data = json.load(f)
        
        # Extract required fields
        project_name = project_data.get("projectTitle", "Unknown Project")
        project_brief = project_data.get("projectBrief", "")
        
        if not project_brief:
            raise ValueError("Project brief is empty in project data file")
        
        logger.info(f"Loaded project: {project_name}")
        logger.info(f"Brief length: {len(project_brief)} characters")
        
        return {"title": project_name, "brief": project_brief}
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in project data file: {e}")
    except Exception as e:
        raise ValueError(f"Error loading project data: {e}")

def load_transcript_data() -> Dict[str, Any]:
    """Load transcript data from the analyzed directory."""
    if not ANALYZED_DIR.exists():
        raise FileNotFoundError(f"Analyzed directory not found at: {ANALYZED_DIR}")
    
    # Find transcript JSON files in the analyzed directory
    transcript_files = list(ANALYZED_DIR.glob("*.transcript.json"))
    
    if not transcript_files:
        raise FileNotFoundError(f"No transcript files (*.transcript.json) found in: {ANALYZED_DIR}")
    
    if len(transcript_files) > 1:
        logger.warning(f"Multiple transcript files found in {ANALYZED_DIR}:")
        for f in transcript_files:
            logger.warning(f"  - {f.name}")
        logger.warning("Using the first one found...")
    
    transcript_path = transcript_files[0]
    
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_data = json.load(f)
        
        logger.info(f"Loaded transcript from: {transcript_path}")
        
        # Basic validation
        if "words" not in transcript_data:
            raise ValueError("Invalid transcript format: missing 'words' field")
        
        word_count = len([w for w in transcript_data["words"] if w.get("word") != "**SILENCE**"])
        timecode_offset = transcript_data.get("timecode_offset_frames", 0)
        
        logger.info(f"Transcript contains {word_count} words")
        logger.info(f"Timecode offset: {timecode_offset} frames")
        
        return transcript_data
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in transcript file: {e}")
    except Exception as e:
        raise ValueError(f"Error loading transcript: {e}")

def load_existing_timeline(timeline_path: Path) -> Dict[str, Any]:
    """Load existing timeline JSON from file."""
    try:
        with open(timeline_path, "r", encoding="utf-8") as f:
            timeline_data = json.load(f)
        
        logger.info(f"Loaded existing timeline from: {timeline_path}")
        
        # Basic validation
        if "timeline" not in timeline_data or "tracks" not in timeline_data:
            raise ValueError("Invalid timeline format: missing required fields")
        
        timeline_info = timeline_data.get("timeline", {})
        tracks = timeline_data.get("tracks", [])
        
        total_clips = sum(len(track.get("clips", [])) for track in tracks)
        duration = timeline_data.get("summary", {}).get("timeline_duration_frames", 0)
        
        logger.info(f"Timeline: {timeline_info.get('name', 'Unknown')}")
        logger.info(f"Total tracks: {len(tracks)}")
        logger.info(f"Total clips: {total_clips}")
        logger.info(f"Duration: {duration} frames")
        
        return timeline_data
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in timeline file: {e}")
    except Exception as e:
        raise ValueError(f"Error loading timeline: {e}")

def load_prompts(existing_timeline: Dict[str, Any], transcript_data: Dict[str, Any], 
                user_brief: str, proj_name: str, user_instructions: str) -> Tuple[str, str]:
    """Load system prompt and format user prompt with all required data."""
    system = system_prompt()
    
    # Convert data to JSON strings
    existing_timeline_json = json.dumps(existing_timeline, indent=2)
    transcript_json = json.dumps(transcript_data, indent=2)
    
    user = user_prompt(
        existing_timeline_json=existing_timeline_json,
        transcript_json=transcript_json, 
        brief=user_brief, 
        project_name=proj_name,
        user_instructions=user_instructions
    )
    return system, user

async def process_reedit_async(
    existing_timeline: Dict[str, Any],
    transcript_data: Dict[str, Any], 
    user_brief: str,
    user_instructions: str,
    output_filename: Optional[str] = None,
    streaming_callback: Optional[callable] = None
) -> Dict[str, Any]:
    """Process a timeline re-edit using Claude API with streaming and thinking features."""
    logger.info("Starting timeline re-editing")
    
    try:
        # Initialize Claude client
        api_key = os.environ.get("claude_api_key")
        if not api_key:
            raise ValueError("Claude API key not found. Set claude_api_key in .env file.")
        
        client = Anthropic(api_key=api_key)
        
        # Get prompts
        system_prompt_text, user_prompt_text = load_prompts(
            existing_timeline, transcript_data, user_brief, project_name, user_instructions
        )
        
        # Create a message with streaming
        logger.info("Sending re-edit request to Claude API with thinking enabled")
        
        # Process with streaming
        thinking_content = ""
        response_content = ""
        
        # Create completion with proper streaming handling
        with client.messages.stream(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt_text,
            messages=[{"role": "user", "content": user_prompt_text}],
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
            
            # Add iteration tracking to metadata
            original_duration = existing_timeline.get("summary", {}).get("timeline_duration_frames", 0)
            if "timeline" in result and "metadata" in result["timeline"]:
                result["timeline"]["metadata"]["previous_duration_frames"] = original_duration
                result["timeline"]["metadata"]["edit_iteration"] = result["timeline"]["metadata"].get("edit_iteration", 1) + 1
            
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
        logger.error(f"Error processing re-edit: {str(e)}")
        return {"error": str(e)}

def process_reedit(
    existing_timeline: Dict[str, Any],
    transcript_data: Dict[str, Any], 
    user_brief: str,
    user_instructions: str,
    output_filename: Optional[str] = None,
    streaming_callback: Optional[callable] = None
) -> Dict[str, Any]:
    """Synchronous wrapper around the async process_reedit function."""
    
    # Get the current event loop or create a new one
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(
        process_reedit_async(
            existing_timeline,
            transcript_data, 
            user_brief,
            user_instructions,
            output_filename, 
            streaming_callback
        )
    )

def run_export_otio():
    """Run the exportotio.py script to export current timeline from DaVinci Resolve."""
    try:
        # Import the exportotio module
        resolveautomation_dir = SCRIPT_DIR.parent / "resolveautomation"
        sys.path.insert(0, str(resolveautomation_dir))
        
        # Import and run the main function from exportotio
        from exportotio import main as export_main
        
        print("Exporting current timeline from DaVinci Resolve...")
        success = export_main()
        
        if success:
            print("✓ Timeline export completed successfully!")
            return True
        else:
            print("✗ Timeline export failed!")
            return False
            
    except ImportError as e:
        print(f"Error importing exportotio module: {e}")
        return False
    except Exception as e:
        print(f"Error during timeline export: {e}")
        return False

def run_import_otio():
    """Run the importotio.py script to import modified timeline back to DaVinci Resolve."""
    try:
        # Import the importotio module
        resolveautomation_dir = SCRIPT_DIR.parent / "resolveautomation"
        sys.path.insert(0, str(resolveautomation_dir))
        
        # Import and run the main function from importotio
        from importotio import main as import_main
        
        print("Importing modified timeline back to DaVinci Resolve...")
        success = import_main()
        
        if success:
            print("✓ Timeline import completed successfully!")
            return True
        else:
            print("✗ Timeline import failed!")
            return False
            
    except ImportError as e:
        print(f"Error importing importotio module: {e}")
        return False
    except Exception as e:
        print(f"Error during timeline import: {e}")
        return False

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
    try:
        print("=== DaVinci Resolve Re-editing Workflow ===")
        print("This will export current timeline, apply edits, and re-import")
        print()
        
        # Step 1: Export current timeline from DaVinci Resolve
        print("STEP 1: Exporting current timeline from DaVinci Resolve")
        print("="*60)
        export_success = run_export_otio()
        
        if not export_success:
            print("❌ Failed to export timeline from DaVinci Resolve")
            print("Please ensure:")
            print("- DaVinci Resolve is running")
            print("- A timeline is currently active")
            print("- Scripting is enabled in DaVinci Resolve")
            exit(1)
        
        print("\nSTEP 2: Loading project data and transcript")
        print("="*60)
        
        # Load project data
        print("Loading project data...")
        project_data = load_project_data()
        project_title = project_data["title"]
        user_brief = project_data["brief"]
        
        print(f"✓ Project: {project_title}")
        print(f"✓ Brief loaded ({len(user_brief)} characters)")
        
        # Load transcript data
        print("\nLoading transcript...")
        transcript_data = load_transcript_data()
        timecode_offset = transcript_data.get("timecode_offset_frames", 0)
        print(f"✓ Transcript loaded from: {ANALYZED_DIR}")
        print(f"✓ Timecode offset: {timecode_offset} frames")
        
        print("\nSTEP 3: Looking for timeline data to re-edit")
        print("="*60)
        
        # First check for existing edited timelines
        timeline_path = find_existing_timeline_json()
        
        if timeline_path:
            existing_timeline = load_existing_timeline(timeline_path)
            print(f"✓ Found existing edited timeline: {timeline_path.name}")
        else:
            # Look for the exported JSON from step 1
            print("No existing edited timeline found, using newly exported timeline...")
            timeline_ref_dir = PROJECT_ROOT / "data" / "timelineprocessing" / "timeline_ref"
            ref_json_files = list(timeline_ref_dir.glob("*.json"))
            
            if not ref_json_files:
                print("❌ No timeline JSON found from export")
                print("Export may have failed - please check DaVinci Resolve")
                exit(1)
            
            ref_timeline_path = ref_json_files[0]  # Use the most recent one
            existing_timeline = load_existing_timeline(ref_timeline_path)
            print(f"✓ Using exported timeline: {ref_timeline_path.name}")
        
        print("\nSTEP 4: Get re-editing instructions")
        print("="*60)
        print("What changes would you like to make to the current timeline?")
        print("Examples:")
        print("  - Remove all clips from speaker A")
        print("  - Make the timeline 30 seconds shorter")
        print("  - Add more content about 'creativity'")
        print("  - Reorder clips to put the introduction first")
        print("  - Replace the ending with a stronger conclusion")
        print("-"*60)
        
        user_instructions = input("Enter your re-editing instructions: ").strip()
        
        if not user_instructions:
            print("❌ No instructions provided. Exiting.")
            exit(1)
        
        print(f"\n✓ Instructions: {user_instructions}")
        
        print("\nSTEP 5: Processing re-edit with AI")
        print("="*60)
        
        # Generate output filename
        current_iteration = existing_timeline.get("timeline", {}).get("metadata", {}).get("edit_iteration", 1)
        output_filename = generate_reedit_filename(project_title, current_iteration + 1)
        
        print(f"Processing setup:")
        print(f"  • Project: {project_title}")
        print(f"  • Instructions: {user_instructions}")
        print(f"  • Output: {output_filename.name}")
        
        print("\nStarting Claude re-editing with thinking enabled...\n")
        
        # Process with streaming to console
        result = process_reedit(
            existing_timeline,
            transcript_data, 
            user_brief,
            user_instructions,
            output_filename=str(output_filename),
            streaming_callback=stream_to_console
        )
        
        print("\n\nRe-editing complete.")
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            # Extract timeline information
            timeline_info = result.get("timeline", {})
            tracks = result.get("tracks", [])
            summary = result.get("summary", {})
            metadata = timeline_info.get("metadata", {})
            
            print(f"✅ Modified timeline: {timeline_info.get('name', 'Unknown')}")
            print(f"✓ Total tracks: {summary.get('total_tracks', 0)}")
            print(f"✓ Total clips: {summary.get('total_clips', 0)}")
            print(f"✓ New duration: {summary.get('timeline_duration_frames', 0)} frames")
            
            # Show duration change
            prev_duration = metadata.get("previous_duration_frames", 0)
            new_duration = summary.get("timeline_duration_frames", 0)
            duration_change = new_duration - prev_duration
            change_sign = "+" if duration_change > 0 else ""
            print(f"✓ Duration change: {change_sign}{duration_change} frames")
            
            print(f"✓ Edit iteration: {metadata.get('edit_iteration', 1)}")
            print(f"✓ Output saved to: {output_filename}")
            
            # Show track breakdown
            for track in tracks:
                track_name = track.get("name", "Unknown Track")
                track_kind = track.get("kind", "Unknown")
                clip_count = len(track.get("clips", []))
                print(f"  - {track_name} ({track_kind}): {clip_count} clips")
            
            # Step 6: Import modified timeline back to DaVinci Resolve
            print(f"\nSTEP 6: Importing modified timeline back to DaVinci Resolve")
            print("="*60)
            
            import_success = run_import_otio()
            
            if import_success:
                print("\n🎉 WORKFLOW COMPLETED SUCCESSFULLY! 🎉")
                print("Modified timeline is now available in DaVinci Resolve")
                print(f"You can run this script again to make further modifications")
            else:
                print("\n⚠️  Re-editing completed but import failed")
                print("You can manually run importotio.py to import the timeline")
                print("Or check DaVinci Resolve connection and try again")
    
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        print("\nRequired files:")
        print(f"  • Transcript files: {ANALYZED_DIR}/*.transcript.json")
        print(f"  • Project data: {PROJECT_DATA_PATH}")
        print(f"  • DaVinci Resolve timeline (will be exported automatically)")
    except ValueError as e:
        print(f"❌ Data Error: {e}")
    except KeyboardInterrupt:
        print(f"\n❌ Interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        logger.exception("Unexpected error in main execution")
