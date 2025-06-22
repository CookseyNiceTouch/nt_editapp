import os
import sys
import json
import logging
import asyncio
from pathlib import Path
import time
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import glob
import argparse
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
        
        # Parse the JSON response
        try:
            logger.info("Parsing Claude's response as JSON")
            
            # Clean markdown formatting if present
            cleaned_response = response_content.strip()
            if cleaned_response.startswith("```json"):
                # Remove opening ```json
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                # Remove opening ``` (in case it's just ```)
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                # Remove closing ```
                cleaned_response = cleaned_response[:-3]
            
            # Final strip
            cleaned_response = cleaned_response.strip()
            
            result = json.loads(cleaned_response)
            
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
    
    # Check if we're already in an event loop (called from chatbot)
    try:
        loop = asyncio.get_running_loop()
        # We're in an event loop already - need to run in a thread
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                asyncio.run,
                process_reedit_async(
                    existing_timeline,
                    transcript_data, 
                    user_brief,
                    user_instructions,
                    output_filename, 
                    streaming_callback
                )
            )
            return future.result()
    except RuntimeError:
        # No running loop, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
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
        finally:
            loop.close()

def clear_timeline_processing_folders():
    """Clear the contents of timeline_ref and timeline_edited folders to prevent duplicates."""
    try:
        import shutil
        
        # Clear timeline_ref folder
        if TIMELINE_REF_DIR.exists():
            for item in TIMELINE_REF_DIR.iterdir():
                if item.is_file():
                    item.unlink()
                    logger.info(f"Removed file: {item.name}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    logger.info(f"Removed directory: {item.name}")
            print("✓ Cleared timeline_ref folder")
        
        # Clear timeline_edited folder
        if TIMELINE_EDITED_DIR.exists():
            for item in TIMELINE_EDITED_DIR.iterdir():
                if item.is_file():
                    item.unlink()
                    logger.info(f"Removed file: {item.name}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    logger.info(f"Removed directory: {item.name}")
            print("✓ Cleared timeline_edited folder")
        
        # Ensure directories exist
        TIMELINE_REF_DIR.mkdir(parents=True, exist_ok=True)
        TIMELINE_EDITED_DIR.mkdir(parents=True, exist_ok=True)
        
        return True
        
    except Exception as e:
        print(f"⚠ Warning: Could not clear timeline processing folders: {e}")
        logger.warning(f"Failed to clear timeline processing folders: {e}")
        return False

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

def main_reedit_workflow(user_instructions: str = None, silent: bool = False) -> Dict[str, Any]:
    """
    Main re-editing workflow function that can be called programmatically or interactively.
    
    Args:
        user_instructions: The editing instructions. If None, will prompt interactively.
        silent: If True, suppress most print output for programmatic use.
        
    Returns:
        Dict with success status and results or error information.
    """
    def print_if_not_silent(msg: str):
        if not silent:
            print(msg)
    
    try:
        if not silent:
            print("=== DaVinci Resolve Re-editing Workflow ===")
            print("This will export current timeline, apply edits, and re-import")
            print()
        
        # Step 1: Clear timeline processing folders and export current timeline
        print_if_not_silent("STEP 1: Preparing timeline processing environment")
        print_if_not_silent("="*60)
        
        # Clear existing files to prevent confusion
        print_if_not_silent("Clearing timeline processing folders...")
        clear_timeline_processing_folders()
        
        print_if_not_silent("\nExporting current timeline from DaVinci Resolve...")
        export_success = run_export_otio()
        
        if not export_success:
            error_msg = "Failed to export timeline from DaVinci Resolve"
            print_if_not_silent(f"❌ {error_msg}")
            if not silent:
                print("Please ensure:")
                print("- DaVinci Resolve is running")
                print("- A timeline is currently active")
                print("- Scripting is enabled in DaVinci Resolve")
            return {"success": False, "error": error_msg}
        
        print_if_not_silent("\nSTEP 2: Loading project data and transcript")
        print_if_not_silent("="*60)
        
        # Load project data
        print_if_not_silent("Loading project data...")
        project_data = load_project_data()
        project_title = project_data["title"]
        user_brief = project_data["brief"]
        
        print_if_not_silent(f"✓ Project: {project_title}")
        print_if_not_silent(f"✓ Brief loaded ({len(user_brief)} characters)")
        
        # Load transcript data
        print_if_not_silent("\nLoading transcript...")
        transcript_data = load_transcript_data()
        timecode_offset = transcript_data.get("timecode_offset_frames", 0)
        print_if_not_silent(f"✓ Transcript loaded from: {ANALYZED_DIR}")
        print_if_not_silent(f"✓ Timecode offset: {timecode_offset} frames")
        
        print_if_not_silent("\nSTEP 3: Looking for timeline data to re-edit")
        print_if_not_silent("="*60)
        
        # First check for existing edited timelines
        timeline_path = find_existing_timeline_json()
        
        if timeline_path:
            existing_timeline = load_existing_timeline(timeline_path)
            print_if_not_silent(f"✓ Found existing edited timeline: {timeline_path.name}")
        else:
            # Look for the exported JSON from step 1
            print_if_not_silent("No existing edited timeline found, using newly exported timeline...")
            timeline_ref_dir = PROJECT_ROOT / "data" / "timelineprocessing" / "timeline_ref"
            ref_json_files = list(timeline_ref_dir.glob("*.json"))
            
            if not ref_json_files:
                error_msg = "No timeline JSON found from export"
                print_if_not_silent(f"❌ {error_msg}")
                print_if_not_silent("Export may have failed - please check DaVinci Resolve")
                return {"success": False, "error": error_msg}
            
            ref_timeline_path = ref_json_files[0]  # Use the most recent one
            existing_timeline = load_existing_timeline(ref_timeline_path)
            print_if_not_silent(f"✓ Using exported timeline: {ref_timeline_path.name}")
        
        # Get user instructions
        if user_instructions is None:
            print_if_not_silent("\nSTEP 4: Get re-editing instructions")
            print_if_not_silent("="*60)
            print_if_not_silent("What changes would you like to make to the current timeline?")
            print_if_not_silent("Examples:")
            print_if_not_silent("  - Remove all clips from speaker A")
            print_if_not_silent("  - Make the timeline 30 seconds shorter")
            print_if_not_silent("  - Add more content about 'creativity'")
            print_if_not_silent("  - Reorder clips to put the introduction first")
            print_if_not_silent("  - Replace the ending with a stronger conclusion")
            print_if_not_silent("-"*60)
            
            user_instructions = input("Enter your re-editing instructions: ").strip()
            
            if not user_instructions:
                error_msg = "No instructions provided"
                print_if_not_silent(f"❌ {error_msg}. Exiting.")
                return {"success": False, "error": error_msg}
        
        print_if_not_silent(f"\n✓ Instructions: {user_instructions}")
        
        print_if_not_silent("\nSTEP 5: Processing re-edit with AI")
        print_if_not_silent("="*60)
        
        # Generate output filename
        current_iteration = existing_timeline.get("timeline", {}).get("metadata", {}).get("edit_iteration", 1)
        output_filename = generate_reedit_filename(project_title, current_iteration + 1)
        
        print_if_not_silent(f"Processing setup:")
        print_if_not_silent(f"  • Project: {project_title}")
        print_if_not_silent(f"  • Instructions: {user_instructions}")
        print_if_not_silent(f"  • Output: {output_filename.name}")
        
        print_if_not_silent("\nStarting Claude re-editing with thinking enabled...\n")
        
        # Process with streaming to console (only if not silent)
        streaming_callback = stream_to_console if not silent else None
        result = process_reedit(
            existing_timeline,
            transcript_data, 
            user_brief,
            user_instructions,
            output_filename=str(output_filename),
            streaming_callback=streaming_callback
        )
        
        print_if_not_silent("\n\nRe-editing complete.")
        
        if "error" in result:
            print_if_not_silent(f"❌ Error: {result['error']}")
            return {"success": False, "error": result['error']}
        else:
            # Extract timeline information
            timeline_info = result.get("timeline", {})
            tracks = result.get("tracks", [])
            summary = result.get("summary", {})
            metadata = timeline_info.get("metadata", {})
            
            print_if_not_silent(f"✅ Modified timeline: {timeline_info.get('name', 'Unknown')}")
            print_if_not_silent(f"✓ Total tracks: {summary.get('total_tracks', 0)}")
            print_if_not_silent(f"✓ Total clips: {summary.get('total_clips', 0)}")
            print_if_not_silent(f"✓ New duration: {summary.get('timeline_duration_frames', 0)} frames")
            
            # Show duration change
            prev_duration = metadata.get("previous_duration_frames", 0)
            new_duration = summary.get("timeline_duration_frames", 0)
            duration_change = new_duration - prev_duration
            change_sign = "+" if duration_change > 0 else ""
            print_if_not_silent(f"✓ Duration change: {change_sign}{duration_change} frames")
            
            print_if_not_silent(f"✓ Edit iteration: {metadata.get('edit_iteration', 1)}")
            print_if_not_silent(f"✓ Output saved to: {output_filename}")
            
            # Show track breakdown
            if not silent:
                for track in tracks:
                    track_name = track.get("name", "Unknown Track")
                    track_kind = track.get("kind", "Unknown")
                    clip_count = len(track.get("clips", []))
                    print(f"  - {track_name} ({track_kind}): {clip_count} clips")
            
            # Step 6: Import modified timeline back to DaVinci Resolve
            print_if_not_silent(f"\nSTEP 6: Importing modified timeline back to DaVinci Resolve")
            print_if_not_silent("="*60)
            
            import_success = run_import_otio()
            
            if import_success:
                print_if_not_silent("\n🎉 WORKFLOW COMPLETED SUCCESSFULLY! 🎉")
                print_if_not_silent("Modified timeline is now available in DaVinci Resolve")
                print_if_not_silent(f"You can run this script again to make further modifications")
                
                return {
                    "success": True,
                    "timeline_name": timeline_info.get('name', 'Unknown'),
                    "total_tracks": summary.get('total_tracks', 0),
                    "total_clips": summary.get('total_clips', 0),
                    "duration_frames": summary.get('timeline_duration_frames', 0),
                    "duration_change_frames": duration_change,
                    "edit_iteration": metadata.get('edit_iteration', 1),
                    "output_file": str(output_filename),
                    "instructions": user_instructions
                }
            else:
                error_msg = "Re-editing completed but import failed"
                print_if_not_silent(f"\n⚠️  {error_msg}")
                print_if_not_silent("You can manually run importotio.py to import the timeline")
                print_if_not_silent("Or check DaVinci Resolve connection and try again")
                
                return {
                    "success": False,
                    "error": error_msg,
                    "partial_success": True,
                    "timeline_generated": True,
                    "output_file": str(output_filename),
                    "instructions": user_instructions
                }
    
    except FileNotFoundError as e:
        error_msg = f"File Error: {e}"
        print_if_not_silent(f"❌ {error_msg}")
        if not silent:
            print("\nRequired files:")
            print(f"  • Transcript files: {ANALYZED_DIR}/*.transcript.json")
            print(f"  • Project data: {PROJECT_DATA_PATH}")
            print(f"  • DaVinci Resolve timeline (will be exported automatically)")
        return {"success": False, "error": error_msg}
    except ValueError as e:
        error_msg = f"Data Error: {e}"
        print_if_not_silent(f"❌ {error_msg}")
        return {"success": False, "error": error_msg}
    except KeyboardInterrupt:
        error_msg = "Interrupted by user"
        print_if_not_silent(f"\n❌ {error_msg}")
        return {"success": False, "error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected Error: {e}"
        print_if_not_silent(f"❌ {error_msg}")
        logger.exception("Unexpected error in main execution")
        return {"success": False, "error": error_msg}

# Main execution when script is run directly
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="DaVinci Resolve Re-editing Workflow")
    parser.add_argument(
        "--instructions", 
        type=str, 
        help="Re-editing instructions to apply to the timeline"
    )
    parser.add_argument(
        "--silent", 
        action="store_true", 
        help="Run in silent mode with minimal output"
    )
    
    args = parser.parse_args()
    
    # Run the workflow
    result = main_reedit_workflow(
        user_instructions=args.instructions,
        silent=args.silent
    )
    
    # Exit with appropriate code
    if result["success"]:
        exit(0)
    else:
        exit(1)
