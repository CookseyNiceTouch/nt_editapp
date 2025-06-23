#!/usr/bin/env python3
"""
OpenTimelineIO to JSON Converter

Pure converter that takes OTIO files and converts them to JSON format.
No hardcoded paths - designed to be used by datapipeline.py or standalone.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import opentimelineio as otio
except ImportError:
    print("ERROR: OpenTimelineIO not found. Install with: pip install OpenTimelineIO>=0.16.0")
    sys.exit(1)


class OTIOJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle OTIO objects like AnyDictionary."""
    
    def default(self, obj):
        # Handle OTIO AnyDictionary and similar objects
        if hasattr(obj, 'items') and callable(obj.items):
            try:
                return dict(obj.items())
            except:
                pass
        
        # Handle OTIO objects with schema_name
        if hasattr(obj, 'schema_name') and callable(obj.schema_name):
            result = {"type": obj.schema_name()}
            if hasattr(obj, 'name') and obj.name:
                result["name"] = obj.name
            return result
        
        # Handle other dict-like objects
        if hasattr(obj, '__dict__'):
            return str(obj)
        
        # For any other non-serializable object
        return str(obj)


def safe_extract_metadata(metadata_obj: Any) -> Dict[str, Any]:
    """
    Safely extract metadata from OTIO objects.
    
    Args:
        metadata_obj: OTIO metadata object
        
    Returns:
        Clean dictionary of metadata
    """
    if not metadata_obj:
        return {}
    
    try:
        # Try to convert to dict if it has items()
        if hasattr(metadata_obj, 'items') and callable(metadata_obj.items):
            result = {}
            for key, value in metadata_obj.items():
                try:
                    # Recursively handle nested structures
                    if hasattr(value, 'items') and callable(value.items):
                        result[str(key)] = dict(value.items())
                    elif isinstance(value, (list, tuple)):
                        result[str(key)] = [safe_extract_metadata(item) if hasattr(item, 'items') else item for item in value]
                    else:
                        result[str(key)] = value
                except:
                    result[str(key)] = str(value)
            return result
        else:
            return {"_raw": str(metadata_obj)}
    except Exception as e:
        return {"_error": f"Failed to extract metadata: {str(e)}"}


def extract_clip_data(clip: otio.schema.Clip, clip_index: int, fps: float) -> Dict[str, Any]:
    """
    Extract relevant data from an OTIO clip.
    
    Args:
        clip: OTIO clip object
        clip_index: Sequential index of the clip in the timeline
        fps: Frame rate of the timeline
        
    Returns:
        Dictionary containing extracted clip data
    """
    clip_data = {
        "clip_index": clip_index,
        "name": clip.name or f"Clip {clip_index + 1}",
        "metadata": {}
    }
    
    # Extract source range information
    if clip.source_range:
        clip_data["source_range"] = {
            "start_frame": int(clip.source_range.start_time.value),
            "duration_frames": int(clip.source_range.duration.value),
            "end_frame": int(clip.source_range.start_time.value + clip.source_range.duration.value - 1),
            "fps": float(clip.source_range.start_time.rate)
        }
    
    # Extract media reference information
    if clip.media_reference:
        media_ref = {
            "type": clip.media_reference.schema_name()
        }
        
        if hasattr(clip.media_reference, 'target_url') and clip.media_reference.target_url:
            media_ref["target_url"] = clip.media_reference.target_url
            # Extract filename from path
            media_ref["filename"] = Path(clip.media_reference.target_url).name
        
        if hasattr(clip.media_reference, 'available_range') and clip.media_reference.available_range:
            available_range = clip.media_reference.available_range
            media_ref["available_range"] = {
                "start_frame": int(available_range.start_time.value),
                "duration_frames": int(available_range.duration.value),
                "end_frame": int(available_range.start_time.value + available_range.duration.value - 1),
                "fps": float(available_range.start_time.rate)
            }
        
        clip_data["media_reference"] = media_ref
    
    # Extract custom metadata safely
    metadata_dict = safe_extract_metadata(clip.metadata)
    
    # Flatten metadata structure for easier access
    for key, value in metadata_dict.items():
        if isinstance(value, dict):
            # If it's a nested dict, preserve structure but flatten one level
            for subkey, subvalue in value.items():
                clip_data["metadata"][f"{key}_{subkey}"] = subvalue
        else:
            clip_data["metadata"][key] = value
    
    return clip_data


def extract_track_data(track: otio.schema.Track, track_index: int, fps: float) -> Dict[str, Any]:
    """
    Extract relevant data from an OTIO track.
    
    Args:
        track: OTIO track object
        track_index: Sequential index of the track
        fps: Frame rate of the timeline
        
    Returns:
        Dictionary containing extracted track data
    """
    track_data = {
        "track_index": track_index,
        "name": track.name or f"Track {track_index + 1}",
        "kind": str(track.kind),
        "clips": []
    }
    
    # Extract clips from track
    clip_index = 0
    for item in track:
        if isinstance(item, otio.schema.Clip):
            clip_data = extract_clip_data(item, clip_index, fps)
            track_data["clips"].append(clip_data)
            clip_index += 1
        elif isinstance(item, otio.schema.Gap):
            # Optionally include gap information
            gap_data = {
                "type": "gap",
                "clip_index": clip_index,
                "name": item.name or f"Gap {clip_index + 1}",
                "source_range": {
                    "duration_frames": int(item.source_range.duration.value) if item.source_range else 0
                }
            }
            track_data["clips"].append(gap_data)
            clip_index += 1
    
    # Add track metadata safely
    track_data["metadata"] = safe_extract_metadata(track.metadata)
    
    return track_data


def convert_otio_to_json(input_path: str, output_path: Optional[str] = None) -> bool:
    """
    Convert an OTIO file to JSON format.
    
    Args:
        input_path: Path to input OTIO file
        output_path: Path to output JSON file (optional, defaults to same name with .json extension)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        input_file = Path(input_path)
        
        if not input_file.exists():
            print(f"ERROR: Input file does not exist: {input_file}")
            return False
        
        if not input_file.suffix.lower() == '.otio':
            print(f"WARNING: Input file doesn't have .otio extension: {input_file}")
        
        # Determine output path
        if output_path is None:
            output_file = input_file.with_suffix('.json')
        else:
            output_file = Path(output_path)
        
        print(f"Converting OTIO to JSON:")
        print(f"  Input:  {input_file}")
        print(f"  Output: {output_file}")
        
        # Read OTIO file
        timeline = otio.adapters.read_from_file(str(input_file))
        print(f"✓ Loaded timeline: {timeline.name}")
        
        # Convert to JSON structure
        json_data = timeline_to_json_data(timeline)
        
        # Create output directory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False, cls=OTIOJSONEncoder)
        
        print(f"✓ Converted to JSON: {output_file}")
        
        # Print summary
        summary = json_data["summary"]
        print(f"  - Tracks: {summary['total_tracks']}")
        print(f"  - Clips: {summary['total_clips']}")
        print(f"  - Duration: {summary.get('timeline_duration_frames', 0)} frames")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def timeline_to_json_data(timeline: otio.schema.Timeline) -> Dict[str, Any]:
    """
    Convert an OTIO timeline to JSON data structure.
    
    Args:
        timeline: OTIO Timeline object
        
    Returns:
        Dictionary containing timeline data
    """
    if not isinstance(timeline, otio.schema.Timeline):
        raise ValueError("Input must be an OTIO Timeline object")
    
    # Determine timeline FPS - use first track's first clip's rate, or default to 24
    fps = 24.0
    try:
        for track in timeline.tracks:
            for item in track:
                if isinstance(item, otio.schema.Clip) and item.source_range:
                    fps = float(item.source_range.start_time.rate)
                    break
            if fps != 24.0:  # Found a rate
                break
    except:
        pass  # Use default 24fps
    
    # Extract timeline metadata safely
    timeline_metadata = safe_extract_metadata(timeline.metadata)
    
    # Extract timeline data
    timeline_data = {
        "schema_version": "1.0",
        "otio_schema_version": otio.__version__,
        "timeline": {
            "name": timeline.name or "Untitled Timeline",
            "fps": fps,
            "metadata": timeline_metadata
        },
        "tracks": [],
        "summary": {
            "total_tracks": len(timeline.tracks),
            "total_clips": 0,
            "timeline_duration_frames": 0
        }
    }
    
    # Calculate timeline duration
    try:
        timeline_duration = timeline.duration()
        timeline_data["summary"]["timeline_duration_frames"] = int(timeline_duration.value)
    except:
        pass  # Duration calculation failed
    
    # Extract tracks and clips
    total_clips = 0
    for track_index, track in enumerate(timeline.tracks):
        if isinstance(track, otio.schema.Track):
            track_data = extract_track_data(track, track_index, fps)
            timeline_data["tracks"].append(track_data)
            total_clips += len([clip for clip in track_data["clips"] if clip.get("type") != "gap"])
    
    timeline_data["summary"]["total_clips"] = total_clips
    
    return timeline_data


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Convert OpenTimelineIO files to JSON format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python otio2json.py timeline.otio
  python otio2json.py timeline.otio output.json
  python otio2json.py /path/to/timeline.otio /path/to/output.json
        """
    )
    
    parser.add_argument('input', help='Input OTIO file path')
    parser.add_argument('output', nargs='?', help='Output JSON file path (optional)')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    args = parser.parse_args()
    
    print("=== OTIO to JSON Converter ===")
    
    success = convert_otio_to_json(args.input, args.output)
    
    if success:
        print("\n=== Conversion completed successfully! ===")
        sys.exit(0)
    else:
        print("\n=== Conversion failed! ===")
        sys.exit(1)


# Adapter metadata for OTIO plugin system
__version__ = "1.0.0"
__author__ = "NiceTouch"
__description__ = "OTIO to JSON converter"


if __name__ == "__main__":
    main()
