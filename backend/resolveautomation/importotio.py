#!/usr/bin/env python3
"""
Interactive script to import timeline files (OTIO/FCPXML/AAF) into DaVinci Resolve.

This script imports a timeline from OTIO, FCPXML, or AAF files without importing source clips,
replicating the manual File > Import > Timeline functionality.

Supported formats:
- OpenTimelineIO (.otio)
- Final Cut Pro XML (.fcpxml)
- Avid Authoring Format (.aaf)
"""

import sys
import os

# =============================================================================
# CONFIGURABLE IMPORT SETTINGS
# =============================================================================
# These settings can be easily modified for testing different import behaviors
# Based on documented ImportTimelineFromFile parameters

IMPORT_SOURCE_CLIPS = False        # Bool: whether to import source clips into media pool
SOURCE_CLIPS_PATH = ""             # string: filesystem path to search for source clips
SOURCE_CLIPS_FOLDERS = []          # List: Media Pool folder objects to search for clips

# Note: interlaceProcessing is only valid for AAF import and has been omitted as requested
# Note: timelineName is set per-import based on user input

# =============================================================================

def get_file_path():
    """Get file path from user input with validation."""
    print("Supported file formats:")
    print("- OpenTimelineIO (.otio)")
    print("- Final Cut Pro XML (.fcpxml)")
    print("- Avid Authoring Format (.aaf)")
    print()
    
    while True:
        file_path = input("Enter the path to your timeline file: ").strip()
        
        # Remove quotes if user copied path with quotes
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]
        elif file_path.startswith("'") and file_path.endswith("'"):
            file_path = file_path[1:-1]
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"ERROR: File not found at: {file_path}")
            print("Please check the path and try again.")
            continue
        
        # Check file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in ['.otio', '.fcpxml', '.aaf']:
            print(f"ERROR: Unsupported file format: {file_ext}")
            print("Supported formats: .otio, .fcpxml, .aaf")
            continue
        
        return file_path, file_ext

def get_timeline_name():
    """Get timeline name from user input."""
    print()
    timeline_name = input("Enter timeline name (press Enter for 'default'): ").strip()
    if not timeline_name:
        timeline_name = "default"
    return timeline_name

def get_import_options(file_ext, timeline_name):
    """Get import options using documented ImportTimelineFromFile parameters."""
    
    # Use global configurable settings for consistent behavior across all formats
    import_options = {
        "timelineName": timeline_name,                # string: name of timeline to be created
        "importSourceClips": IMPORT_SOURCE_CLIPS,     # Bool: whether to import source clips (True by default in API)
        "sourceClipsPath": SOURCE_CLIPS_PATH,         # string: filesystem path to search for source clips
        "sourceClipsFolders": SOURCE_CLIPS_FOLDERS,   # List: Media Pool folder objects to search for clips
        # Note: interlaceProcessing is only valid for AAF import, omitting as requested
    }
    
    print(f"Using standardized import options for {file_ext.upper()}")
    
    return import_options

def check_media_pool_for_clips(media_pool):
    """Check if there are clips in the media pool and provide guidance."""
    try:
        current_folder = media_pool.GetCurrentFolder()
        clips = current_folder.GetClipList()
        
        if not clips or len(clips) == 0:
            print("⚠️  WARNING: No clips found in current media pool folder!")
            print("   For best FCPXML import results:")
            print("   1. Import your source media into the media pool FIRST")
            print("   2. Then import the FCPXML file")
            print("   This helps Resolve properly link timeline clips to media")
            print()
            return False
        else:
            print(f"✓ Found {len(clips)} clip(s) in media pool folder '{current_folder.GetName()}'")
            return True
            
    except Exception as e:
        print(f"Could not check media pool contents: {e}")
        return None

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
        
        # Get file path and timeline name from user
        file_path, file_ext = get_file_path()
        timeline_name = get_timeline_name()
        
        print(f"✓ File selected: {file_path}")
        print(f"✓ File type: {file_ext.upper()}")
        print(f"✓ Timeline name: {timeline_name}")
        print()
        
        # Check media pool contents for FCPXML/AAF imports
        if file_ext in ['.fcpxml', '.aaf']:
            print("Checking media pool for source clips...")
            has_clips = check_media_pool_for_clips(media_pool)
            if has_clips is False:
                proceed = input("Continue with import anyway? (y/N): ").strip().lower()
                if proceed not in ['y', 'yes']:
                    print("Import cancelled. Please import your source media first.")
                    return False
        
        # Check for existing timeline with same name
        try:
            timeline_count = project.GetTimelineCount()
            for i in range(1, timeline_count + 1):
                existing_timeline = project.GetTimelineByIndex(i)
                if existing_timeline and existing_timeline.GetName() == timeline_name:
                    print(f"WARNING: Timeline '{timeline_name}' already exists!")
                    overwrite = input("Do you want to continue anyway? (y/N): ").strip().lower()
                    if overwrite not in ['y', 'yes']:
                        print("Import cancelled by user.")
                        return False
                    break
        except Exception as e:
            print(f"Warning: Could not check existing timelines: {e}")
        
        # Set up import options based on file type
        import_options = get_import_options(file_ext, timeline_name)
        
        print("Import options:")
        for key, value in import_options.items():
            print(f"  {key}: {value}")
        print()
        
        # Import the timeline
        print(f"Importing {file_ext.upper()} timeline...")
        timeline = media_pool.ImportTimelineFromFile(file_path, import_options)
        
        # If import fails, try with importSourceClips enabled as fallback
        if not timeline:
            print("Initial import failed. Trying with source clips import enabled...")
            fallback_options = import_options.copy()
            fallback_options["importSourceClips"] = True
            timeline = media_pool.ImportTimelineFromFile(file_path, fallback_options)
            
            if timeline:
                print("✓ Fallback import method succeeded")
            else:
                print("✗ All import methods failed")
        
        if timeline:
            print(f"SUCCESS: Timeline '{timeline.GetName()}' imported successfully!")
            print()
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
                print("  Video track contents:")
                for track_idx in range(1, video_tracks + 1):
                    items = timeline.GetItemListInTrack("video", track_idx)
                    print(f"    Track {track_idx}: {len(items)} item(s)")
            
            if audio_tracks > 0:
                print("  Audio track contents:")
                for track_idx in range(1, audio_tracks + 1):
                    items = timeline.GetItemListInTrack("audio", track_idx)
                    print(f"    Track {track_idx}: {len(items)} item(s)")
            
            return True
        else:
            print("ERROR: Failed to import timeline from file!")
            print()
            print("Possible issues:")
            print(f"- {file_ext.upper()} file format is not compatible with this version of DaVinci Resolve")
            print(f"- Timeline name '{timeline_name}' conflicts with existing timeline")
            print("- Media referenced in file is not found in the project")
            
            if file_ext == '.fcpxml':
                print("- FCPXML files contain absolute file paths that may not match your system")
                print("- The original media files may be in different locations")
                print("- Try importing the source media into your media pool first, then retry")
                print("- Check that media file names in your project match those in the FCPXML")
            
            if file_ext == '.aaf':
                print("- AAF files may have interlace processing requirements")
                print("- The original media files may be in different locations than expected")
                print("- Try importing the source media into your media pool first, then retry")
                print("- Check that media file names and timecode match those in the AAF")
                print("- AAF files from older Avid versions may have compatibility issues")
            
            print("- File contains unsupported elements or codec")
            print("- Check DaVinci Resolve console for more detailed error messages")
            
            # Show existing timelines for reference
            try:
                timeline_count = project.GetTimelineCount()
                if timeline_count > 0:
                    print(f"Existing timelines in project ({timeline_count}):")
                    for i in range(1, timeline_count + 1):
                        existing_timeline = project.GetTimelineByIndex(i)
                        if existing_timeline:
                            print(f"  {i}. {existing_timeline.GetName()}")
                else:
                    print("No existing timelines in project.")
            except Exception as e:
                print(f"Could not retrieve timeline information: {e}")
            
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
    print("=== DaVinci Resolve Timeline Import Tool ===")
    print("Interactive import for OTIO, FCPXML, and AAF files")
    print()
    
    success = main()
    
    print()
    if success:
        print("=== Import completed successfully! ===")
        sys.exit(0)
    else:
        print("=== Import failed! ===")
        sys.exit(1)
