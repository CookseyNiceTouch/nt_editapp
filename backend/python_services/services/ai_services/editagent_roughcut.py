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
from dotenv import load_dotenv
import anthropic
from anthropic import Anthropic
from jsonschema import validate
from prompts.prompts_roughcut import system_prompt, user_prompt

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
    """Find existing JSON file in timeline_ref directory to match the name."""
    try:
        # Look for JSON files in timeline_ref directory
        json_files = list(TIMELINE_REF_DIR.glob("*.json"))
        
        if json_files:
            if len(json_files) > 1:
                logger.warning(f"Multiple JSON files found in {TIMELINE_REF_DIR}:")
                for f in json_files:
                    logger.warning(f"  - {f.name}")
                logger.warning("Using the first one found...")
            
            existing_json = json_files[0]
            logger.info(f"Found existing timeline JSON: {existing_json.name}")
            return existing_json
        else:
            logger.info(f"No existing JSON files found in {TIMELINE_REF_DIR}")
            return None
            
    except Exception as e:
        logger.warning(f"Error checking for existing JSON files: {e}")
        return None

def generate_output_filename(project_title: str, match_existing: bool = True) -> Path:
    """Generate output filename, optionally matching existing timeline JSON names."""
    
    # Ensure output directory exists
    TIMELINE_EDITED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Try to match existing timeline JSON filename
    if match_existing:
        existing_json = find_existing_timeline_json()
        if existing_json:
            # Use the same filename as the existing JSON in timeline_ref
            filename = existing_json.name
            output_path = TIMELINE_EDITED_DIR / filename
            logger.info(f"Matching existing timeline name: {filename}")
            return output_path
    
    # Fallback: Generate new timestamped filename
    # Clean project title for filename (remove invalid characters)
    clean_title = "".join(c for c in project_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_title = clean_title.replace(' ', '_')
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create filename
    filename = f"{clean_title}_edit_{timestamp}.json"
    output_path = TIMELINE_EDITED_DIR / filename
    
    logger.info(f"Generated new filename: {filename}")
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

def load_prompts(transcript_data: Dict[str, Any], user_brief: str, proj_name: str) -> Tuple[str, str]:
    """Load system prompt and format user prompt with transcript data and brief."""
    system = system_prompt()
    transcript_json = json.dumps(transcript_data, indent=2)
    user = user_prompt(transcript_json=transcript_json, brief=user_brief, project_name=proj_name)
    return system, user

def analyze_transcript_quality(transcript_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze transcript quality based on confidence scores and provide insights."""
    words = transcript_data.get("words", [])
    
    # Filter out silence markers for confidence analysis
    word_entries = [word for word in words if word.get("word") != "**SILENCE**"]
    
    if not word_entries:
        return {"error": "No word entries found for analysis"}
    
    # Extract confidence scores
    confidences = [word.get("confidence", 0) for word in word_entries if word.get("confidence") is not None]
    
    if not confidences:
        logger.warning("No confidence scores found in transcript")
        return {"warning": "No confidence scores available"}
    
    # Calculate statistics
    avg_confidence = sum(confidences) / len(confidences)
    min_confidence = min(confidences)
    max_confidence = max(confidences)
    
    # Count low confidence words
    low_confidence_count = len([c for c in confidences if c < 0.7])
    very_low_confidence_count = len([c for c in confidences if c < 0.5])
    
    # Find words with lowest confidence
    low_confidence_words = [(word["word"], word["confidence"], word["speaker"]) 
                           for word in word_entries 
                           if word.get("confidence", 0) < 0.7]
    
    # Speaker confidence analysis
    speaker_confidence = {}
    for word in word_entries:
        speaker = word.get("speaker", "Unknown")
        confidence = word.get("confidence", 0)
        if speaker not in speaker_confidence:
            speaker_confidence[speaker] = []
        speaker_confidence[speaker].append(confidence)
    
    # Calculate average confidence per speaker
    for speaker in speaker_confidence:
        speaker_confidence[speaker] = sum(speaker_confidence[speaker]) / len(speaker_confidence[speaker])
    
    quality_report = {
        "total_words": len(word_entries),
        "avg_confidence": round(avg_confidence, 3),
        "min_confidence": round(min_confidence, 3),
        "max_confidence": round(max_confidence, 3),
        "low_confidence_words": low_confidence_count,
        "very_low_confidence_words": very_low_confidence_count,
        "low_confidence_percentage": round((low_confidence_count / len(confidences)) * 100, 1),
        "speaker_confidence": {k: round(v, 3) for k, v in speaker_confidence.items()},
        "worst_words": low_confidence_words[:10]  # Top 10 worst confidence words
    }
    
    # Log quality insights
    logger.info(f"Transcript Quality Analysis:")
    logger.info(f"  Average confidence: {quality_report['avg_confidence']}")
    logger.info(f"  Low confidence words (<0.7): {quality_report['low_confidence_words']} ({quality_report['low_confidence_percentage']}%)")
    
    if quality_report['avg_confidence'] < 0.8:
        logger.warning(f"Below average transcript quality detected. Consider audio quality improvements.")
    
    if quality_report['low_confidence_words'] > 0:
        logger.warning(f"Found {quality_report['low_confidence_words']} words with low confidence - may need manual review")
    
    for speaker, conf in quality_report['speaker_confidence'].items():
        if conf < 0.7:
            logger.warning(f"Speaker '{speaker}' has low average confidence: {conf}")
    
    return quality_report

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
        system_prompt, user_prompt = load_prompts(transcript_data, user_brief, project_name)
        
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
    
    # Check if we're already in an event loop (called from chatbot)
    try:
        loop = asyncio.get_running_loop()
        # We're in an event loop already - need to run in a thread
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                asyncio.run,
                process_transcript_async(
                    transcript_data, 
                    user_brief,
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
                process_transcript_async(
                    transcript_data, 
                    user_brief,
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

def run_import_otio():
    """Run the importotio.py script to import generated timeline to DaVinci Resolve."""
    try:
        # Import the importotio module
        resolveautomation_dir = SCRIPT_DIR.parent / "resolveautomation"
        sys.path.insert(0, str(resolveautomation_dir))
        
        # Import and run the main function from importotio
        from importotio import main as import_main
        
        print("Importing timeline to DaVinci Resolve...")
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

def main_roughcut_workflow(silent: bool = False) -> Dict[str, Any]:
    """
    Main rough cut generation workflow function that can be called programmatically or interactively.
    
    Args:
        silent: If True, suppress most print output for programmatic use.
        
    Returns:
        Dict with success status and results or error information.
    """
    def print_if_not_silent(msg: str):
        if not silent:
            print(msg)
    
    try:
        if not silent:
            print("=== AI Rough Cut Generator and Import Workflow ===")
            print("This will generate a rough cut from transcript and import to DaVinci Resolve")
            print()
        
        print_if_not_silent("STEP 1: Preparing timeline processing environment")
        print_if_not_silent("="*60)
        
        # Clear existing files to prevent confusion
        print_if_not_silent("Clearing timeline processing folders...")
        clear_timeline_processing_folders()
        
        print_if_not_silent("\nSTEP 2: Loading project data and transcript")
        print_if_not_silent("="*60)
        
        # Load project data first
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
        
        print_if_not_silent("\nSTEP 3: Analyzing transcript quality")
        print_if_not_silent("="*60)
        quality_report = analyze_transcript_quality(transcript_data)
        
        if "error" not in quality_report and "warning" not in quality_report:
            print_if_not_silent(f"✓ Transcript Quality Report:")
            print_if_not_silent(f"  • Total words: {quality_report['total_words']}")
            print_if_not_silent(f"  • Average confidence: {quality_report['avg_confidence']}")
            print_if_not_silent(f"  • Low confidence words: {quality_report['low_confidence_words']} ({quality_report['low_confidence_percentage']}%)")
            
            if quality_report['worst_words']:
                print_if_not_silent(f"  • Words needing attention: {len(quality_report['worst_words'])} words with confidence < 0.7")
                if quality_report['avg_confidence'] < 0.8:
                    print_if_not_silent("  ⚠ Consider reviewing audio quality or manual transcript verification")
            
            print_if_not_silent(f"  • Speaker confidence:")
            for speaker, conf in quality_report['speaker_confidence'].items():
                status = "✓" if conf >= 0.8 else "⚠" if conf >= 0.7 else "✗"
                print_if_not_silent(f"    {status} {speaker}: {conf}")
        
        # Generate output filename (matching existing timeline if available)
        output_filename = generate_output_filename(project_title, match_existing=True)
        
        print_if_not_silent(f"\nSTEP 4: Generating rough cut timeline")
        print_if_not_silent("="*60)
        
        print_if_not_silent(f"Processing setup:")
        print_if_not_silent(f"  • Project: {project_title}")
        print_if_not_silent(f"  • Brief preview: {user_brief[:100]}...")
        print_if_not_silent(f"  • Output directory: {TIMELINE_EDITED_DIR}")
        print_if_not_silent(f"  • Output filename: {output_filename.name}")
        
        # Show timeline integration info
        existing_json = find_existing_timeline_json()
        if existing_json:
            print_if_not_silent(f"  • Matching existing timeline: {existing_json.name}")
            print_if_not_silent(f"  • Integration: This edit will replace the existing JSON in timeline_edited/")
        else:
            print_if_not_silent(f"  • Creating new edit sequence")
        
        print_if_not_silent("\nStarting Claude processing with thinking enabled...\n")
        
        # Process with streaming to console (only if not silent)
        streaming_callback = stream_to_console if not silent else None
        result = process_transcript(
            transcript_data, 
            user_brief, 
            output_filename=str(output_filename),
            streaming_callback=streaming_callback
        )
        
        print_if_not_silent("\n\nRough cut generation complete.")
        
        if "error" in result:
            print_if_not_silent(f"❌ Error: {result['error']}")
            return {"success": False, "error": result['error']}
        else:
            # Extract timeline information
            timeline_info = result.get("timeline", {})
            tracks = result.get("tracks", [])
            summary = result.get("summary", {})
            
            print_if_not_silent(f"✓ Generated timeline: {timeline_info.get('name', 'Unknown')}")
            print_if_not_silent(f"✓ Total tracks: {summary.get('total_tracks', 0)}")
            print_if_not_silent(f"✓ Total clips: {summary.get('total_clips', 0)}")
            print_if_not_silent(f"✓ Timeline duration: {summary.get('timeline_duration_frames', 0)} frames")
            print_if_not_silent(f"✓ Output saved to: {output_filename}")
            
            # Show track breakdown
            if not silent:
                for track in tracks:
                    track_name = track.get("name", "Unknown Track")
                    track_kind = track.get("kind", "Unknown")
                    clip_count = len(track.get("clips", []))
                    print(f"  - {track_name} ({track_kind}): {clip_count} clips")
            
            # Analyze confidence in the generated clips
            all_clips = []
            for track in tracks:
                all_clips.extend(track.get("clips", []))
            
            avg_clip_confidence = None
            if all_clips:
                clip_confidences = []
                for clip in all_clips:
                    metadata = clip.get("metadata", {})
                    if "avg_confidence" in metadata:
                        clip_confidences.append(metadata["avg_confidence"])
                
                if clip_confidences:
                    avg_clip_confidence = sum(clip_confidences) / len(clip_confidences)
                    print_if_not_silent(f"\n✓ Average clip confidence: {avg_clip_confidence:.3f}")
                    
                    low_conf_clips = [i for i, conf in enumerate(clip_confidences) if conf < 0.7]
                    if low_conf_clips:
                        print_if_not_silent(f"⚠ Clips with low confidence: {len(low_conf_clips)} (review recommended)")
            
            # Step 5: Import timeline to DaVinci Resolve
            print_if_not_silent(f"\nSTEP 5: Importing timeline to DaVinci Resolve")
            print_if_not_silent("="*60)
            
            import_success = run_import_otio()
            
            if import_success:
                print_if_not_silent("\n🎉 ROUGH CUT WORKFLOW COMPLETED SUCCESSFULLY! 🎉")
                print_if_not_silent("Timeline is now available in DaVinci Resolve")
                print_if_not_silent("You can run editagent_reedit.py to make further modifications")
                
                return {
                    "success": True,
                    "timeline_name": timeline_info.get('name', 'Unknown'),
                    "total_tracks": summary.get('total_tracks', 0),
                    "total_clips": summary.get('total_clips', 0),
                    "duration_frames": summary.get('timeline_duration_frames', 0),
                    "output_file": str(output_filename),
                    "avg_clip_confidence": avg_clip_confidence,
                    "quality_report": quality_report
                }
            else:
                error_msg = "Rough cut generated but import failed"
                print_if_not_silent(f"\n⚠️  {error_msg}")
                print_if_not_silent("Timeline JSON is available in timeline_edited/ directory")
                print_if_not_silent("You can manually run importotio.py to import the timeline")
                print_if_not_silent("Or check DaVinci Resolve connection and try again")
                
                return {
                    "success": False,
                    "error": error_msg,
                    "partial_success": True,
                    "timeline_generated": True,
                    "output_file": str(output_filename)
                }
    
    except FileNotFoundError as e:
        error_msg = f"File Error: {e}"
        print_if_not_silent(f"❌ {error_msg}")
        if not silent:
            print("\nRequired files:")
            print(f"  • Transcript files: {ANALYZED_DIR}/*.transcript.json")
            print(f"  • Project data: {PROJECT_DATA_PATH}")
        return {"success": False, "error": error_msg}
    except ValueError as e:
        error_msg = f"Data Error: {e}"
        print_if_not_silent(f"❌ {error_msg}")
        return {"success": False, "error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected Error: {e}"
        print_if_not_silent(f"❌ {error_msg}")
        logger.exception("Unexpected error in main execution")
        return {"success": False, "error": error_msg}

# Main execution when script is run directly
if __name__ == "__main__":
    # Run the workflow function
    result = main_roughcut_workflow(silent=False)
    
    # Exit with appropriate code
    if result["success"]:
        exit(0)
    else:
        exit(1)
