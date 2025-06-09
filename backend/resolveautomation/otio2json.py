#!/usr/bin/env python3
"""
OpenTimelineIO to JSON Adapter

Adapter to extract relevant clip data from OTIO timelines and export to JSON format.
Only extracts essential clip information for timeline editing workflows.
"""

import sys
import json
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


def write_to_string(input_otio: otio.schema.Timeline) -> str:
    """
    Convert an OTIO timeline to JSON string containing relevant clip data.
    
    Args:
        input_otio: OTIO Timeline object
        
    Returns:
        JSON string containing extracted clip data
    """
    if not isinstance(input_otio, otio.schema.Timeline):
        raise ValueError("Input must be an OTIO Timeline object")
    
    # Determine timeline FPS - use first track's first clip's rate, or default to 24
    fps = 24.0
    try:
        for track in input_otio.tracks:
            for item in track:
                if isinstance(item, otio.schema.Clip) and item.source_range:
                    fps = float(item.source_range.start_time.rate)
                    break
            if fps != 24.0:  # Found a rate
                break
    except:
        pass  # Use default 24fps
    
    # Extract timeline metadata safely
    timeline_metadata = safe_extract_metadata(input_otio.metadata)
    
    # Extract timeline data
    timeline_data = {
        "schema_version": "1.0",
        "otio_schema_version": otio.__version__,
        "timeline": {
            "name": input_otio.name or "Untitled Timeline",
            "fps": fps,
            "metadata": timeline_metadata
        },
        "tracks": [],
        "summary": {
            "total_tracks": len(input_otio.tracks),
            "total_clips": 0,
            "timeline_duration_frames": 0
        }
    }
    
    # Calculate timeline duration
    try:
        timeline_duration = input_otio.duration()
        timeline_data["summary"]["timeline_duration_frames"] = int(timeline_duration.value)
    except:
        pass  # Duration calculation failed
    
    # Extract tracks and clips
    total_clips = 0
    for track_index, track in enumerate(input_otio.tracks):
        if isinstance(track, otio.schema.Track):
            track_data = extract_track_data(track, track_index, fps)
            timeline_data["tracks"].append(track_data)
            total_clips += len([clip for clip in track_data["clips"] if clip.get("type") != "gap"])
    
    timeline_data["summary"]["total_clips"] = total_clips
    
    # Convert to JSON with custom encoder
    return json.dumps(timeline_data, indent=2, ensure_ascii=False, cls=OTIOJSONEncoder)


def write_to_file(input_otio: otio.schema.Timeline, filepath: str) -> None:
    """
    Write OTIO timeline to JSON file containing relevant clip data.
    
    Args:
        input_otio: OTIO Timeline object
        filepath: Output file path
    """
    json_string = write_to_string(input_otio)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(json_string)


def read_from_string(input_str: str) -> otio.schema.Timeline:
    """
    Read JSON string and convert to OTIO timeline.
    Note: This is a basic implementation for round-trip compatibility.
    
    Args:
        input_str: JSON string
        
    Returns:
        OTIO Timeline object
    """
    raise NotImplementedError(
        "Reading from JSON to OTIO is not implemented in this adapter. "
        "Use the json2otio.py module for JSON to OTIO conversion."
    )


def read_from_file(filepath: str) -> otio.schema.Timeline:
    """
    Read JSON file and convert to OTIO timeline.
    Note: This is a basic implementation for round-trip compatibility.
    
    Args:
        filepath: Input file path
        
    Returns:
        OTIO Timeline object
    """
    raise NotImplementedError(
        "Reading from JSON to OTIO is not implemented in this adapter. "
        "Use the json2otio.py module for JSON to OTIO conversion."
    )


# Adapter metadata for OTIO plugin system
__version__ = "1.0.0"
__author__ = "NiceTouch"
__description__ = "OTIO to JSON adapter for extracting clip data"


if __name__ == "__main__":
    # Basic CLI functionality for testing
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert OTIO timeline to JSON with clip data")
    parser.add_argument("input_file", help="Input OTIO file path")
    parser.add_argument("-o", "--output", help="Output JSON file path (optional)")
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON to console")
    
    args = parser.parse_args()
    
    try:
        # Read OTIO file
        timeline = otio.adapters.read_from_file(args.input_file)
        
        if args.pretty:
            # Print to console
            json_output = write_to_string(timeline)
            print(json_output)
        else:
            # Determine output path
            if args.output:
                output_path = args.output
            else:
                # Default output directory (relative path)
                output_dir = Path("../../data/edits/fromNLE")
                output_dir.mkdir(parents=True, exist_ok=True)
                
                # Use same filename as input but with .json extension
                input_filename = Path(args.input_file).stem  # Gets filename without extension
                output_path = output_dir / f"{input_filename}.json"
            
            # Write to file
            write_to_file(timeline, str(output_path))
            print(f"✓ Converted {args.input_file} to {output_path}")
            
            # Print summary
            json_data = json.loads(write_to_string(timeline))
            summary = json_data["summary"]
            print(f"  - Tracks: {summary['total_tracks']}")
            print(f"  - Clips: {summary['total_clips']}")
            print(f"  - Duration: {summary.get('timeline_duration_frames', 0)} frames")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
