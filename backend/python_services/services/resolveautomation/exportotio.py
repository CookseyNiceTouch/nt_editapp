#!/usr/bin/env python3
"""
Automated script to export the current timeline from DaVinci Resolve to OpenTimelineIO (OTIO) format.

This script automatically exports the currently active timeline from DaVinci Resolve
to OTIO format, saving it to the timeline_ref directory with the timeline name as filename.
After successful export, it automatically converts the OTIO to JSON format for editing.

Export location: ../../data/timelineprocessing/timeline_ref/

No user interaction required - runs completely automated.
"""

import sys
import os
import re
from pathlib import Path

# =============================================================================
# CONFIGURABLE EXPORT SETTINGS
# =============================================================================
# These settings can be easily modified for testing different export behaviors

# Target directory for OTIO exports (relative to script location)
EXPORT_TARGET_DIR = os.path.join("..", "..", "data", "timelineprocessing", "timeline_ref")

# Export options - based on DaVinci Resolve API ExportTimelineToFile parameters
EXPORT_OPTIONS = {
    # Add any export-specific options here when they become available in the API
    # Currently the API documentation is limited for OTIO export options
}

# =============================================================================

def sanitize_filename(filename):
    """Sanitize filename by removing or replacing invalid characters."""
    # Remove invalid characters for Windows/Linux filesystems
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove trailing dots and spaces
    sanitized = sanitized.rstrip('. ')
    
    # Limit length to reasonable size
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    
    return sanitized

def get_export_directory():
    """Get and validate the export directory path."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))  # Go up from backend/resolveautomation to project root
    export_dir = os.path.join(project_root, "data", "timelineprocessing", "timeline_ref")
    export_dir = os.path.normpath(export_dir)
    
    # Create directory if it doesn't exist
    try:
        os.makedirs(export_dir, exist_ok=True)
        print(f"✓ Export directory: {export_dir}")
        return export_dir
    except Exception as e:
        print(f"ERROR: Could not create export directory: {export_dir}")
        print(f"Error: {e}")
        return None

def get_timeline_info(timeline):
    """Get detailed information about the timeline for display."""
    try:
        info = {
            'name': timeline.GetName(),
            'duration_frames': timeline.GetEndFrame() - timeline.GetStartFrame() + 1,
            'start_frame': timeline.GetStartFrame(),
            'end_frame': timeline.GetEndFrame(),
            'start_timecode': timeline.GetStartTimecode(),
            'video_tracks': timeline.GetTrackCount("video"),
            'audio_tracks': timeline.GetTrackCount("audio"),
            'subtitle_tracks': timeline.GetTrackCount("subtitle")
        }
        return info
    except Exception as e:
        print(f"Warning: Could not get complete timeline information: {e}")
        return {'name': timeline.GetName() if timeline else 'Unknown'}

def display_timeline_info(timeline_info):
    """Display timeline information for logging."""
    print("Timeline details:")
    for key, value in timeline_info.items():
        formatted_key = key.replace('_', ' ').title()
        print(f"  {formatted_key}: {value}")

def export_timeline_to_otio(timeline, export_path):
    """Export the timeline to OTIO format."""
    try:
        print(f"Exporting timeline to: {export_path}")
        
        # Use the timeline's Export method with EXPORT_OTIO constant
        # This was added in DaVinci Resolve 18.5 Beta 3
        success = timeline.Export(export_path, resolve.EXPORT_OTIO)
        
        if success:
            print("✓ Timeline exported successfully!")
            return True
        else:
            print("✗ Export failed - API returned False")
            return False
            
    except Exception as e:
        print(f"ERROR during export: {e}")
        return False

def convert_otio_to_json():
    """Convert the exported OTIO file to JSON format using the otio2json converter."""
    try:
        # Import the otio2json module
        script_dir = Path(__file__).parent.resolve()
        sys.path.insert(0, str(script_dir))
        
        # Import the conversion function from otio2json
        from otio2json import convert_timeline_ref_to_json
        
        # Run the conversion
        return convert_timeline_ref_to_json()
        
    except ImportError as e:
        print(f"Error importing otio2json module: {e}")
        return False
    except Exception as e:
        print(f"Error during OTIO to JSON conversion: {e}")
        return False

def main():
    try:
        # Import DaVinci Resolve API
        print("Importing DaVinci Resolve API...")
        import DaVinciResolveScript as dvr_script
        print("✓ DaVinciResolveScript module imported successfully")
        
        # Connect to DaVinci Resolve
        print("Connecting to DaVinci Resolve...")
        global resolve
        resolve = dvr_script.scriptapp("Resolve")
        if not resolve:
            print("ERROR: Could not connect to DaVinci Resolve!")
            print("Make sure:")
            print("- DaVinci Resolve is running")
            print("- Scripting is enabled in DaVinci Resolve preferences")
            print("- You're running DaVinci Resolve Studio (free version has limited API access)")
            return False
        
        print("✓ Connected to DaVinci Resolve successfully")
        
        # Check if EXPORT_OTIO constant is available (requires DaVinci Resolve 18.5 Beta 3+)
        if not hasattr(resolve, 'EXPORT_OTIO'):
            print("ERROR: OTIO export is not supported in this version of DaVinci Resolve!")
            print("OTIO export requires DaVinci Resolve 18.5 Beta 3 or later.")
            print("Please update your DaVinci Resolve version to use this feature.")
            return False
        
        print("✓ OTIO export capability confirmed")
        
        # Get the current project
        project_manager = resolve.GetProjectManager()
        project = project_manager.GetCurrentProject()
        if not project:
            print("ERROR: No project is currently open!")
            print("Please open a project in DaVinci Resolve first.")
            return False
        
        print(f"✓ Connected to project: {project.GetName()}")
        
        # Get export directory
        export_dir = get_export_directory()
        if not export_dir:
            return False
        
        # Get the current timeline automatically
        current_timeline = project.GetCurrentTimeline()
        if not current_timeline:
            print("ERROR: No timeline is currently active!")
            print("Please select a timeline in DaVinci Resolve first.")
            return False
        
        print(f"✓ Current timeline: {current_timeline.GetName()}")
        
        # Get timeline information
        timeline_info = get_timeline_info(current_timeline)
        display_timeline_info(timeline_info)
        
        # Generate filename from timeline name for natural workflow
        timeline_name = timeline_info['name']
        sanitized_name = sanitize_filename(timeline_name)
        filename = f"{sanitized_name}.otio"
        export_path = os.path.join(export_dir, filename)
        
        # Handle existing files automatically (overwrite)
        if os.path.exists(export_path):
            print(f"Overwriting existing file: {filename}")
        
        print(f"Export filename: {filename}")
        print(f"Timeline name: {timeline_name}")
        
        # Perform the export automatically
        print("Starting export...")
        success = export_timeline_to_otio(current_timeline, export_path)
        
        if success:
            # Verify file was created and get size
            if os.path.exists(export_path):
                file_size = os.path.getsize(export_path)
                print(f"✓ Export completed successfully!")
                print(f"  File: {export_path}")
                print(f"  Size: {file_size} bytes")
                
                # Basic validation - OTIO files should contain certain text
                try:
                    with open(export_path, 'r', encoding='utf-8') as f:
                        content = f.read(1000)  # Read first 1000 chars
                        if 'OTIO_SCHEMA' in content or 'Timeline' in content:
                            print("✓ File appears to be valid OTIO format")
                        else:
                            print("⚠️  Warning: File may not be valid OTIO format")
                            return False
                except Exception as e:
                    print(f"⚠️  Warning: Could not validate file format: {e}")
                    return False
                
                # Automatically convert OTIO to JSON for editing workflow
                print()
                print("Converting OTIO to JSON for editing workflow...")
                json_success = convert_otio_to_json()
                
                if json_success:
                    print("✓ OTIO to JSON conversion completed successfully!")
                    return True
                else:
                    print("⚠️  Warning: OTIO export succeeded but JSON conversion failed")
                    print("You can manually run otio2json.py to convert the OTIO file")
                    return True  # Still return True since OTIO export succeeded
            else:
                print("ERROR: Export reported success but file was not created!")
                return False
        else:
            print("ERROR: Export failed!")
            print()
            print("Possible issues:")
            print("- DaVinci Resolve version doesn't support OTIO export (requires 18.5 Beta 3 or later)")
            print("- Timeline contains unsupported elements for OTIO export")
            print("- File permissions issue in export directory")
            print("- Timeline is corrupted or has missing media")
            print("- Check DaVinci Resolve console for more detailed error messages")
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
        print("\nExport cancelled by user.")
        return False
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {str(e)}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("=== DaVinci Resolve OTIO Export Tool (Automated) ===")
    print("Exporting current timeline to OpenTimelineIO format and converting to JSON")
    print()
    
    success = main()
    
    print()
    if success:
        print("=== Export and conversion completed successfully! ===")
        print("OTIO file and JSON ready for editing workflow")
        sys.exit(0)
    else:
        print("=== Export failed! ===")
        sys.exit(1)
