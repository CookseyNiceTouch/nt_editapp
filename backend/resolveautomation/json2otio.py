#!/usr/bin/env python3
"""
JSON to OpenTimelineIO Adapter

Adapter to take JSON clip data and apply it to a reference OTIO timeline.
Follows the same structure as otio2json.py for seamless workflow.
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


def load_json_data(filepath: str) -> Dict[str, Any]:
    """
    Load and validate JSON file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON data
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Basic validation
        required_fields = ["timeline", "tracks", "summary"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        return data
    except Exception as e:
        print(f"Error loading JSON: {e}")
        sys.exit(1)


def safe_set_metadata(otio_object, metadata_dict: Dict[str, Any]) -> None:
    """
    Safely set metadata on an OTIO object, filtering out problematic keys.
    
    Args:
        otio_object: OTIO object to set metadata on
        metadata_dict: Dictionary of metadata to set
    """
    if not metadata_dict:
        return
    
    # First pass - check if any keys are problematic
    has_problematic_keys = False
    for key in metadata_dict.keys():
        if not isinstance(key, str) or not key.strip():
            has_problematic_keys = True
            break
        if any(char in key for char in ['\n', '\r', '\t', '\0']):
            has_problematic_keys = True
            break
        if key.startswith('_'):
            has_problematic_keys = True
            break
    
    # If we found problematic keys, skip metadata entirely
    if has_problematic_keys:
        return
    
    # Filter out any remaining edge cases
    clean_metadata = {}
    for key, value in metadata_dict.items():
        clean_key = key.strip()
        if clean_key and len(clean_key) > 0:
            clean_metadata[clean_key] = value
    
    # Only set if we have clean metadata
    if clean_metadata:
        try:
            otio_object.metadata = clean_metadata
        except Exception as e:
            # If we still get errors, just skip metadata for this object
            return


def apply_clip_modifications(otio_clip: otio.schema.Clip, json_clip: Dict[str, Any]) -> None:
    """
    Apply JSON clip data to an OTIO clip.
    
    Args:
        otio_clip: OTIO clip to modify
        json_clip: JSON clip data to apply
    """
    # Update clip name if different
    if "name" in json_clip and json_clip["name"] != otio_clip.name:
        otio_clip.name = json_clip["name"]
    
    # Update source range if provided
    if "source_range" in json_clip:
        source_range = json_clip["source_range"]
        if all(key in source_range for key in ["start_frame", "duration_frames", "fps"]):
            # Create new source range from JSON data
            start_time = otio.opentime.RationalTime(
                int(source_range["start_frame"]), 
                float(source_range["fps"])
            )
            duration = otio.opentime.RationalTime(
                int(source_range["duration_frames"]), 
                float(source_range["fps"])
            )
            otio_clip.source_range = otio.opentime.TimeRange(start_time, duration)
    
    # Update media reference if provided
    if "media_reference" in json_clip:
        media_ref_data = json_clip["media_reference"]
        
        # Only update target_url if provided and different
        if "target_url" in media_ref_data and hasattr(otio_clip.media_reference, 'target_url'):
            if media_ref_data["target_url"] != otio_clip.media_reference.target_url:
                otio_clip.media_reference.target_url = media_ref_data["target_url"]
        
        # Update available range if provided
        if "available_range" in media_ref_data and hasattr(otio_clip.media_reference, 'available_range'):
            avail_range = media_ref_data["available_range"]
            if all(key in avail_range for key in ["start_frame", "duration_frames", "fps"]):
                start_time = otio.opentime.RationalTime(
                    int(avail_range["start_frame"]), 
                    float(avail_range["fps"])
                )
                duration = otio.opentime.RationalTime(
                    int(avail_range["duration_frames"]), 
                    float(avail_range["fps"])
                )
                otio_clip.media_reference.available_range = otio.opentime.TimeRange(start_time, duration)
    
    # Update metadata using safe method
    if "metadata" in json_clip and json_clip["metadata"]:
        # Get existing metadata or create new
        existing_metadata = dict(otio_clip.metadata) if otio_clip.metadata else {}
        
        # Process new metadata from JSON
        for key, value in json_clip["metadata"].items():
            # Skip invalid keys
            if not isinstance(key, str) or not key.strip():
                continue
                
            # Handle flattened metadata (reverse the flattening from otio2json)
            if "_" in key and len(key.split("_", 1)) == 2:
                parts = key.split("_", 1)
                parent_key, sub_key = parts[0], parts[1]
                
                # Skip if either part is empty
                if not parent_key.strip() or not sub_key.strip():
                    continue
                
                if parent_key not in existing_metadata:
                    existing_metadata[parent_key] = {}
                
                if isinstance(existing_metadata[parent_key], dict):
                    existing_metadata[parent_key][sub_key] = value
                else:
                    # Convert to dict if it's not already
                    existing_metadata[parent_key] = {sub_key: value}
            else:
                existing_metadata[key] = value
        
        # Use safe metadata setting
        safe_set_metadata(otio_clip, existing_metadata)


def create_clip_from_json(json_clip: Dict[str, Any]) -> otio.schema.Clip:
    """
    Create a new OTIO clip from JSON data.
    
    Args:
        json_clip: JSON clip data
        
    Returns:
        New OTIO clip object
    """
    # Create basic clip
    clip = otio.schema.Clip(name=json_clip.get("name", "Clip"))
    
    # Set source range if provided
    if "source_range" in json_clip:
        source_range = json_clip["source_range"]
        if all(key in source_range for key in ["start_frame", "duration_frames", "fps"]):
            start_time = otio.opentime.RationalTime(
                int(source_range["start_frame"]), 
                float(source_range["fps"])
            )
            duration = otio.opentime.RationalTime(
                int(source_range["duration_frames"]), 
                float(source_range["fps"])
            )
            clip.source_range = otio.opentime.TimeRange(start_time, duration)
    
    # Set media reference if provided
    if "media_reference" in json_clip:
        media_ref_data = json_clip["media_reference"]
        
        # Create external reference
        target_url = media_ref_data.get("target_url", "")
        media_ref = otio.schema.ExternalReference(target_url=target_url)
        
        # Set available range if provided
        if "available_range" in media_ref_data:
            avail_range = media_ref_data["available_range"]
            if all(key in avail_range for key in ["start_frame", "duration_frames", "fps"]):
                start_time = otio.opentime.RationalTime(
                    int(avail_range["start_frame"]), 
                    float(avail_range["fps"])
                )
                duration = otio.opentime.RationalTime(
                    int(avail_range["duration_frames"]), 
                    float(avail_range["fps"])
                )
                media_ref.available_range = otio.opentime.TimeRange(start_time, duration)
        
        clip.media_reference = media_ref
    
    # Set metadata if provided - use safe method
    if "metadata" in json_clip and json_clip["metadata"]:
        metadata_dict = {}
        
        # Process metadata from JSON (handle flattened metadata)
        for key, value in json_clip["metadata"].items():
            # Skip invalid keys
            if not isinstance(key, str) or not key.strip():
                continue
                
            if "_" in key and len(key.split("_", 1)) == 2:
                parts = key.split("_", 1)
                parent_key, sub_key = parts[0], parts[1]
                
                # Skip if either part is empty
                if not parent_key.strip() or not sub_key.strip():
                    continue
                
                if parent_key not in metadata_dict:
                    metadata_dict[parent_key] = {}
                
                metadata_dict[parent_key][sub_key] = value
            else:
                metadata_dict[key] = value
        
        # Use safe metadata setting
        safe_set_metadata(clip, metadata_dict)
    
    return clip


def match_clips_by_index(otio_track: otio.schema.Track, json_track: Dict[str, Any]) -> List[tuple]:
    """
    Match OTIO clips with JSON clips by index, creating new clips when needed.
    
    Args:
        otio_track: OTIO track
        json_track: JSON track data
        
    Returns:
        List of (otio_clip, json_clip, action) tuples where action is 'modify' or 'create'
    """
    matches = []
    otio_clips = [item for item in otio_track if isinstance(item, otio.schema.Clip)]
    json_clips = [clip for clip in json_track["clips"] if clip.get("type") != "gap"]
    
    # Match existing clips and identify clips to create
    for json_clip in json_clips:
        clip_index = json_clip.get("clip_index", 0)
        if clip_index < len(otio_clips):
            # Existing clip - modify it
            matches.append((otio_clips[clip_index], json_clip, 'modify'))
        else:
            # New clip - create it
            matches.append((None, json_clip, 'create'))
    
    return matches


def apply_track_modifications(otio_track: otio.schema.Track, json_track: Dict[str, Any]) -> None:
    """
    Apply JSON track data to an OTIO track, creating new clips as needed.
    
    Args:
        otio_track: OTIO track to modify
        json_track: JSON track data to apply
    """
    # Update track name if different
    if "name" in json_track and json_track["name"] != otio_track.name:
        otio_track.name = json_track["name"]
    
    # Match and update/create clips
    clip_matches = match_clips_by_index(otio_track, json_track)
    
    # Track which clips we need to add
    clips_to_add = []
    
    for otio_clip, json_clip, action in clip_matches:
        if action == 'modify':
            # Modify existing clip
            apply_clip_modifications(otio_clip, json_clip)
        elif action == 'create':
            # Create new clip
            try:
                new_clip = create_clip_from_json(json_clip)
                clips_to_add.append((json_clip.get("clip_index", 0), new_clip))
            except Exception as e:
                print(f"Warning: Failed to create clip {json_clip.get('name', 'Unknown')}: {e}")
                continue
    
    # Add new clips to the track in the correct order
    clips_to_add.sort(key=lambda x: x[0])  # Sort by clip_index
    for clip_index, new_clip in clips_to_add:
        # Insert at the correct position or append if at end
        if clip_index < len(otio_track):
            otio_track.insert(clip_index, new_clip)
        else:
            otio_track.append(new_clip)
    
    # Update track metadata if provided - use regular dict
    if "metadata" in json_track and json_track["metadata"]:
        if not otio_track.metadata:
            otio_track.metadata = {}
        
        for key, value in json_track["metadata"].items():
            # Skip empty keys
            if key and isinstance(key, str) and key.strip() != "":
                otio_track.metadata[key] = value


def apply_json_to_timeline(reference_timeline: otio.schema.Timeline, json_data: Dict[str, Any]) -> otio.schema.Timeline:
    """
    Apply JSON modifications to a reference timeline.
    
    Args:
        reference_timeline: Reference OTIO timeline
        json_data: JSON data to apply
        
    Returns:
        Modified timeline
    """
    # Create a deep copy of the reference timeline
    modified_timeline = reference_timeline.deepcopy()
    
    # Update timeline name if provided and different
    timeline_info = json_data.get("timeline", {})
    if "name" in timeline_info and timeline_info["name"] != modified_timeline.name:
        modified_timeline.name = timeline_info["name"]
    
    # Update timeline metadata if provided - use regular dict
    if "metadata" in timeline_info and timeline_info["metadata"]:
        if not modified_timeline.metadata:
            modified_timeline.metadata = {}
        
        for key, value in timeline_info["metadata"].items():
            # Skip empty keys
            if key and isinstance(key, str) and key.strip() != "":
                modified_timeline.metadata[key] = value
    
    # Match and update tracks
    json_tracks = json_data.get("tracks", [])
    otio_tracks = [track for track in modified_timeline.tracks if isinstance(track, otio.schema.Track)]
    
    for json_track in json_tracks:
        track_index = json_track.get("track_index", 0)
        if track_index < len(otio_tracks):
            apply_track_modifications(otio_tracks[track_index], json_track)
        else:
            print(f"Warning: JSON track index {track_index} exceeds OTIO tracks count ({len(otio_tracks)})")
    
    return modified_timeline


def convert_json_to_otio(json_filepath: str, reference_otio_filepath: str, output_filepath: str = None) -> bool:
    """
    Convert JSON to OTIO using a reference timeline.
    
    Args:
        json_filepath: Path to JSON file
        reference_otio_filepath: Path to reference OTIO file
        output_filepath: Output OTIO file path (optional)
        
    Returns:
        True if successful
    """
    try:
        # Load JSON data
        json_data = load_json_data(json_filepath)
        print(f"✓ Loaded JSON: {json_filepath}")
        
        # Load reference timeline
        reference_timeline = otio.adapters.read_from_file(reference_otio_filepath)
        print(f"✓ Loaded reference OTIO: {reference_otio_filepath}")
        
        # Apply modifications
        modified_timeline = apply_json_to_timeline(reference_timeline, json_data)
        print(f"✓ Applied JSON modifications to timeline")
        
        # Determine output path
        if not output_filepath:
            json_name = Path(json_filepath).stem
            output_dir = Path("../../data/edits/toNLE")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_filepath = output_dir / f"{json_name}_modified.otio"
        
        # Write modified timeline
        otio.adapters.write_to_file(modified_timeline, str(output_filepath))
        print(f"✓ Wrote modified timeline: {output_filepath}")
        
        # Print summary
        summary = json_data.get("summary", {})
        print(f"  - Tracks: {summary.get('total_tracks', 'unknown')}")
        print(f"  - Clips: {summary.get('total_clips', 'unknown')}")
        print(f"  - Duration: {summary.get('timeline_duration_frames', 'unknown')} frames")
        
        return True
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False


# Adapter metadata
__version__ = "1.0.0"
__author__ = "NiceTouch"
__description__ = "JSON to OTIO adapter using reference timeline"


if __name__ == "__main__":
    # CLI functionality
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert JSON to OTIO using reference timeline")
    parser.add_argument("json_file", help="Input JSON file path")
    parser.add_argument("reference_otio", help="Reference OTIO file path")
    parser.add_argument("-o", "--output", help="Output OTIO file path (optional)")
    
    args = parser.parse_args()
    
    success = convert_json_to_otio(args.json_file, args.reference_otio, args.output)
    
    if not success:
        sys.exit(1)
