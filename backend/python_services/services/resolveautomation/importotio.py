#!/usr/bin/env python3
"""
Automated script to convert JSON to OTIO and import timeline files into DaVinci Resolve.

This script automatically finds JSON files in timeline_edited directory, converts them to OTIO,
and then imports the resulting timeline into DaVinci Resolve without importing source clips.

Import source: ../../data/timelineprocessing/timeline_edited/

No user interaction required - runs completely automated.
"""

import sys
import os
import glob
import json
from pathlib import Path

# =============================================================================
# CONFIGURABLE IMPORT SETTINGS
# =============================================================================
# These settings can be easily modified for testing different import behaviors
# Based on documented ImportTimelineFromFile parameters

IMPORT_SOURCE_CLIPS = False        # Bool: whether to import source clips into media pool
SOURCE_CLIPS_PATH = ""             # string: filesystem path to search for source clips
SOURCE_CLIPS_FOLDERS = []          # List: Media Pool folder objects to search for clips

# Target directory for OTIO imports (relative to script location)
IMPORT_SOURCE_DIR = os.path.join("..", "..", "data", "timelineprocessing", "timeline_edited")

# =============================================================================

def get_import_directory():
    """Get and validate the import directory path."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))  # Go up from backend/resolveautomation to project root
    import_dir = os.path.join(project_root, "data", "timelineprocessing", "timeline_edited")
    import_dir = os.path.normpath(import_dir)
    
    if not os.path.exists(import_dir):
        print(f"ERROR: Import directory does not exist: {import_dir}")
        print("Please run json2otio.py first to create modified OTIO files.")
        return None
    
    print(f"✓ Import directory: {import_dir}")
    return import_dir

def convert_json_to_otio(import_dir):
    """Convert JSON to OTIO using the json2otio converter, return OTIO file path."""
    try:
        # Import the json2otio module
        script_dir = Path(__file__).parent.resolve()
        sys.path.insert(0, str(script_dir))
        
        # Import the conversion function from json2otio
        from json2otio import apply_json_edits_to_timeline
        
        print("Converting JSON to OTIO...")
        # Run the conversion
        success = apply_json_edits_to_timeline()
        
        if not success:
            print("ERROR: JSON to OTIO conversion failed")
            return None
        
        # Find the generated OTIO file
        otio_pattern = os.path.join(import_dir, "*.otio")
        otio_files = glob.glob(otio_pattern)
        
        if not otio_files:
            print("ERROR: No OTIO file generated after JSON conversion")
            return None
        
        # Use the most recently created OTIO file
        otio_file = max(otio_files, key=os.path.getmtime)
        print(f"✓ Generated OTIO file: {os.path.basename(otio_file)}")
        return otio_file
        
    except ImportError as e:
        print(f"Error importing json2otio module: {e}")
        return None
    except Exception as e:
        print(f"Error during JSON to OTIO conversion: {e}")
        return None

def find_or_convert_otio_file(import_dir):
    """Find existing OTIO file or convert from JSON in the import directory."""
    # First, look for JSON files to convert
    json_pattern = os.path.join(import_dir, "*.json")
    json_files = glob.glob(json_pattern)
    
    if json_files:
        if len(json_files) > 1:
            print(f"WARNING: Multiple JSON files found in {import_dir}:")
            for f in json_files:
                print(f"  - {os.path.basename(f)}")
            print("Converting the first one found...")
        
        json_file = json_files[0]
        print(f"✓ Found JSON file: {os.path.basename(json_file)}")
        
        # Convert JSON to OTIO
        return convert_json_to_otio(import_dir)
    
    # Fallback: look for existing OTIO files
    otio_pattern = os.path.join(import_dir, "*.otio")
    otio_files = glob.glob(otio_pattern)
    
    if not otio_files:
        print(f"ERROR: No JSON or OTIO files found in {import_dir}")
        print("Please run editagent_roughcut.py or editagent_reedit.py first to create JSON files.")
        return None
    
    if len(otio_files) > 1:
        print(f"WARNING: Multiple OTIO files found in {import_dir}:")
        for f in otio_files:
            print(f"  - {os.path.basename(f)}")
        print("Using the most recent one...")
    
    # Use the most recently created OTIO file
    otio_file = max(otio_files, key=os.path.getmtime)
    print(f"✓ Found existing OTIO file: {os.path.basename(otio_file)}")
    return otio_file

def generate_timeline_name(otio_file_path):
    """Generate timeline name from OTIO filename."""
    filename = os.path.basename(otio_file_path)
    timeline_name = os.path.splitext(filename)[0]
    print(f"✓ Timeline name: {timeline_name}")
    return timeline_name

def get_import_options(timeline_name):
    """Get import options using documented ImportTimelineFromFile parameters."""
    
    # Use global configurable settings for consistent behavior
    import_options = {
        "timelineName": timeline_name,                # string: name of timeline to be created
        "importSourceClips": IMPORT_SOURCE_CLIPS,     # Bool: whether to import source clips (False by default for our workflow)
        "sourceClipsPath": SOURCE_CLIPS_PATH,         # string: filesystem path to search for source clips
        "sourceClipsFolders": SOURCE_CLIPS_FOLDERS,   # List: Media Pool folder objects to search for clips
    }
    
    print("Import options:")
    for key, value in import_options.items():
        print(f"  {key}: {value}")
    
    return import_options

def get_unique_timeline_name(project, base_timeline_name):
    """Get a unique timeline name by appending suffix if needed."""
    try:
        timeline_count = project.GetTimelineCount()
        existing_names = set()
        
        # Collect all existing timeline names
        for i in range(1, timeline_count + 1):
            existing_timeline = project.GetTimelineByIndex(i)
            if existing_timeline:
                existing_names.add(existing_timeline.GetName())
        
        # If base name doesn't exist, use it
        if base_timeline_name not in existing_names:
            return base_timeline_name
        
        # Find a unique name by appending suffix
        suffix = 1
        while True:
            candidate_name = f"{base_timeline_name} ({suffix})"
            if candidate_name not in existing_names:
                print(f"Timeline '{base_timeline_name}' already exists - using '{candidate_name}' instead")
                return candidate_name
            suffix += 1
            
            # Safety check to prevent infinite loop
            if suffix > 1000:
                print(f"Warning: Could not find unique name after 1000 attempts, using timestamp suffix")
                import time
                timestamp_suffix = int(time.time())
                return f"{base_timeline_name}_{timestamp_suffix}"
                
    except Exception as e:
        print(f"Warning: Could not check existing timelines: {e}")
        # Fallback to timestamp suffix
        import time
        timestamp_suffix = int(time.time())
        return f"{base_timeline_name}_{timestamp_suffix}"

def display_timeline_info(timeline):
    """Display imported timeline information."""
    try:
        print("Timeline details:")
        print(f"  Name: {timeline.GetName()}")
        print(f"  Duration: {timeline.GetEndFrame() - timeline.GetStartFrame() + 1} frames")
        print(f"  Start frame: {timeline.GetStartFrame()}")
        print(f"  End frame: {timeline.GetEndFrame()}")
        print(f"  Start timecode: {timeline.GetStartTimecode()}")
        
        # Get track counts
        video_tracks = timeline.GetTrackCount("video")
        audio_tracks = timeline.GetTrackCount("audio")
        subtitle_tracks = timeline.GetTrackCount("subtitle")
        
        print(f"  Tracks - Video: {video_tracks}, Audio: {audio_tracks}, Subtitle: {subtitle_tracks}")
        
        # List timeline items if there are any
        if video_tracks > 0:
            total_video_items = 0
            for track_idx in range(1, video_tracks + 1):
                items = timeline.GetItemListInTrack("video", track_idx)
                total_video_items += len(items)
            print(f"  Total video items: {total_video_items}")
        
        if audio_tracks > 0:
            total_audio_items = 0
            for track_idx in range(1, audio_tracks + 1):
                items = timeline.GetItemListInTrack("audio", track_idx)
                total_audio_items += len(items)
            print(f"  Total audio items: {total_audio_items}")
            
    except Exception as e:
        print(f"Warning: Could not get complete timeline information: {e}")

def main():
    try:
        # Import DaVinci Resolve API
        print("Importing DaVinci Resolve API...")
        import DaVinciResolveScript as dvr_script
        print("✓ DaVinciResolveScript module imported successfully")
        
        # Connect to DaVinci Resolve
        print("Connecting to DaVinci Resolve...")
        resolve = dvr_script.scriptapp("Resolve")
        if not resolve:
            print("ERROR: Could not connect to DaVinci Resolve!")
            print("Make sure:")
            print("- DaVinci Resolve is running")
            print("- Scripting is enabled in DaVinci Resolve preferences")
            print("- You're running DaVinci Resolve Studio (free version has limited API access)")
            return False
        
        print("✓ Connected to DaVinci Resolve successfully")
        
        # Get the current project
        project_manager = resolve.GetProjectManager()
        project = project_manager.GetCurrentProject()
        if not project:
            print("ERROR: No project is currently open!")
            print("Please open a project in DaVinci Resolve first.")
            return False
        
        print(f"✓ Connected to project: {project.GetName()}")
        
        # Get the media pool
        media_pool = project.GetMediaPool()
        current_folder = media_pool.GetCurrentFolder()
        print(f"✓ Current media pool folder: {current_folder.GetName()}")
        print()
        
        # Get import directory
        import_dir = get_import_directory()
        if not import_dir:
            return False
        
        # Find JSON file and convert to OTIO, or use existing OTIO file
        otio_file = find_or_convert_otio_file(import_dir)
        if not otio_file:
            return False
        
        # Generate timeline name from filename
        base_timeline_name = generate_timeline_name(otio_file)
        
        # Get unique timeline name (adds suffix if needed)
        timeline_name = get_unique_timeline_name(project, base_timeline_name)
        
        print(f"✓ File selected: {otio_file}")
        print(f"✓ File type: OTIO")
        print(f"✓ Final timeline name: {timeline_name}")
        print()
        
        # Set up import options
        import_options = get_import_options(timeline_name)
        print()
        
        # Import the timeline automatically
        print("Importing OTIO timeline...")
        timeline = media_pool.ImportTimelineFromFile(otio_file, import_options)
        
        # If import fails, try with importSourceClips enabled as fallback
        if not timeline:
            print("Initial import failed. Trying with source clips import enabled...")
            fallback_options = import_options.copy()
            fallback_options["importSourceClips"] = True
            timeline = media_pool.ImportTimelineFromFile(otio_file, fallback_options)
            
            if timeline:
                print("✓ Fallback import method succeeded")
            else:
                print("✗ All import methods failed")
        
        if timeline:
            print(f"✓ Timeline '{timeline.GetName()}' imported successfully!")
            print()
            display_timeline_info(timeline)
            
            # Verify file size for reference
            try:
                file_size = os.path.getsize(otio_file)
                print(f"  Source file size: {file_size} bytes")
            except Exception as e:
                pass
            
            return True
        else:
            print("ERROR: Failed to import timeline from OTIO file!")
            print()
            print("Possible issues:")
            print("- OTIO file format is not compatible with this version of DaVinci Resolve")
            print(f"- Timeline name '{timeline_name}' conflicts with existing timeline")
            print("- Media referenced in OTIO file is not found in the project")
            print("- OTIO file contains unsupported elements or codec")
            print("- OTIO file may be corrupted or incorrectly formatted")
            print("- Check DaVinci Resolve console for more detailed error messages")
            print()
            print("Troubleshooting:")
            print("- Ensure the original media is imported into your media pool")
            print("- Check that media file paths in the OTIO match your project structure")
            print("- Try importing the source media first, then retry the timeline import")
            print("- Verify the OTIO file was generated correctly by json2otio.py")
            
            return False
            
    except ImportError as e:
        print(f"ERROR: Could not import DaVinciResolveScript module: {e}")
        print("Make sure the DaVinci Resolve scripting environment is properly configured.")
        print("Required environment variables:")
        print("- RESOLVE_SCRIPT_API")
        print("- RESOLVE_SCRIPT_LIB") 
        print("- PYTHONPATH")
        return False
    except KeyboardInterrupt:
        print("\nImport cancelled by user.")
        return False
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {str(e)}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("=== DaVinci Resolve JSON→OTIO→Import Tool (Automated) ===")
    print("Converting JSON to OTIO and importing timeline into DaVinci Resolve")
    print()
    
    success = main()
    
    print()
    if success:
        print("=== Conversion and import completed successfully! ===")
        print("Timeline is now available in DaVinci Resolve")
        sys.exit(0)
    else:
        print("=== Conversion or import failed! ===")
        sys.exit(1)
