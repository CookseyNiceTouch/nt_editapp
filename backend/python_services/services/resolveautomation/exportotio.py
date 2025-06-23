#!/usr/bin/env python3
"""
DaVinci Resolve OTIO Export Tool

Pure exporter that exports the current timeline from DaVinci Resolve to OTIO format.
No hardcoded paths - designed to be used by datapipeline.py or standalone.
"""

import sys
import os
import re
import argparse
from pathlib import Path
from typing import Optional


def sanitize_filename(filename: str) -> str:
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


def get_timeline_info(timeline) -> dict:
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


def display_timeline_info(timeline_info: dict) -> None:
    """Display timeline information for logging."""
    print("Timeline details:")
    for key, value in timeline_info.items():
        formatted_key = key.replace('_', ' ').title()
        print(f"  {formatted_key}: {value}")


def export_timeline_to_otio(resolve_api, timeline, export_path: str) -> bool:
    """Export the timeline to OTIO format."""
    try:
        print(f"Exporting timeline to: {export_path}")
        
        # Use the timeline's Export method with EXPORT_OTIO constant
        # This was added in DaVinci Resolve 18.5 Beta 3
        success = timeline.Export(export_path, resolve_api.EXPORT_OTIO)
        
        if success:
            print("✓ Timeline exported successfully!")
            return True
        else:
            print("✗ Export failed - API returned False")
            return False
            
    except Exception as e:
        print(f"ERROR during export: {e}")
        return False


def export_current_timeline(output_path: Optional[str] = None, timeline_name: Optional[str] = None) -> bool:
    """
    Export the current timeline from DaVinci Resolve to OTIO format.
    
    Args:
        output_path: Path to save the OTIO file (optional, will auto-generate if not provided)
        timeline_name: Specific timeline name to export (optional, uses current timeline if not provided)
        
    Returns:
        True if successful, False otherwise
    """
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
        
        # Get the timeline to export
        if timeline_name:
            # Find timeline by name
            timeline_count = project.GetTimelineCount()
            current_timeline = None
            for i in range(1, timeline_count + 1):
                timeline = project.GetTimelineByIndex(i)
                if timeline and timeline.GetName() == timeline_name:
                    current_timeline = timeline
                    break
            
            if not current_timeline:
                print(f"ERROR: Timeline '{timeline_name}' not found!")
                print("Available timelines:")
                for i in range(1, timeline_count + 1):
                    tl = project.GetTimelineByIndex(i)
                    if tl:
                        print(f"  - {tl.GetName()}")
                return False
        else:
            # Get the current timeline
            current_timeline = project.GetCurrentTimeline()
            if not current_timeline:
                print("ERROR: No timeline is currently active!")
                print("Please select a timeline in DaVinci Resolve first.")
                return False
        
        print(f"✓ Target timeline: {current_timeline.GetName()}")
        
        # Get timeline information
        timeline_info = get_timeline_info(current_timeline)
        display_timeline_info(timeline_info)
        
        # Determine output path
        if output_path is None:
            # Generate filename from timeline name
            sanitized_name = sanitize_filename(timeline_info['name'])
            filename = f"{sanitized_name}.otio"
            output_file = Path.cwd() / filename
        else:
            output_file = Path(output_path)
            # Ensure .otio extension
            if not output_file.suffix.lower() == '.otio':
                output_file = output_file.with_suffix('.otio')
        
        # Create output directory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Handle existing files
        if output_file.exists():
            print(f"Overwriting existing file: {output_file}")
        
        print(f"Export filename: {output_file}")
        print(f"Timeline name: {timeline_info['name']}")
        print()
        
        # Perform the export
        print("Starting export...")
        success = export_timeline_to_otio(resolve, current_timeline, str(output_file))
        
        if success:
            # Verify file was created and get size
            if output_file.exists():
                file_size = output_file.stat().st_size
                print(f"✓ Export completed successfully!")
                print(f"  File: {output_file}")
                print(f"  Size: {file_size} bytes")
                
                # Basic validation - OTIO files should contain certain text
                try:
                    with open(output_file, 'r', encoding='utf-8') as f:
                        content = f.read(1000)  # Read first 1000 chars
                        if 'OTIO_SCHEMA' in content or 'Timeline' in content:
                            print("✓ File appears to be valid OTIO format")
                        else:
                            print("⚠️  Warning: File may not be valid OTIO format")
                            return False
                except Exception as e:
                    print(f"⚠️  Warning: Could not validate file format: {e}")
                    return False
                
                return True
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


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Export timeline from DaVinci Resolve to OpenTimelineIO format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python exportotio.py
  python exportotio.py --output my_timeline.otio
  python exportotio.py --timeline "Timeline 1" --output /path/to/timeline.otio
        """
    )
    
    parser.add_argument('--output', '-o', help='Output OTIO file path (optional)')
    parser.add_argument('--timeline', '-t', help='Specific timeline name to export (optional, uses current timeline)')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    args = parser.parse_args()
    
    print("=== DaVinci Resolve OTIO Export Tool ===")
    print("Exporting timeline to OpenTimelineIO format")
    print()
    
    success = export_current_timeline(args.output, args.timeline)
    
    print()
    if success:
        print("=== Export completed successfully! ===")
        sys.exit(0)
    else:
        print("=== Export failed! ===")
        sys.exit(1)


if __name__ == "__main__":
    main()
