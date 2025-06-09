#!/usr/bin/env python3
"""
JSON to OpenTimelineIO Adapter

Adapter to rebuild OTIO timelines from JSON data created by otio2json.py.
Simple reconstruction with no complex calculations - just rebuild the OTIO structure.
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


def load_project_data() -> Dict[str, Any]:
    """Load project data from projectdata.json for fallback values."""
    try:
        script_dir = Path(__file__).parent.resolve()
        project_root = script_dir.parent.parent
        project_data_path = project_root / "data" / "projectdata.json"
        
        if project_data_path.exists():
            with open(project_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"Warning: Project data not found at {project_data_path}")
            return {}
    except Exception as e:
        print(f"Warning: Could not load project data: {e}")
        return {}


def create_clip_from_json(json_clip: Dict[str, Any]) -> otio.schema.Clip:
    """
    Create an OTIO clip from JSON clip data.
    
    Args:
        json_clip: JSON clip data from otio2json format
        
    Returns:
        OTIO Clip object
    """
    # Create basic clip
    clip = otio.schema.Clip(name=json_clip.get("name", "Clip"))
    
    # Set source range from JSON
    if "source_range" in json_clip:
        source_range = json_clip["source_range"]
        start_time = otio.opentime.RationalTime(
            int(source_range["start_frame"]), 
            float(source_range["fps"])
        )
        duration = otio.opentime.RationalTime(
            int(source_range["duration_frames"]), 
            float(source_range["fps"])
        )
        clip.source_range = otio.opentime.TimeRange(start_time, duration)
    
    # Set media reference from JSON
    if "media_reference" in json_clip:
        media_ref_data = json_clip["media_reference"]
        
        # Create external reference
        target_url = media_ref_data.get("target_url", "")
        media_ref = otio.schema.ExternalReference(target_url=target_url)
        
        # Set available range if provided
        if "available_range" in media_ref_data:
            avail_range = media_ref_data["available_range"]
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
    
    # Set metadata from JSON (excluding text field - only for AI editing)
    if "metadata" in json_clip and json_clip["metadata"]:
        # Process flattened metadata (reverse the flattening from otio2json)
        for key, value in json_clip["metadata"].items():
            # Skip text field - it's only for AI editing purposes, not for OTIO
            if key == "text":
                continue
                
            if "_" in key and len(key.split("_", 1)) == 2:
                parts = key.split("_", 1)
                parent_key, sub_key = parts[0], parts[1]
                
                if parent_key not in clip.metadata:
                    clip.metadata[parent_key] = {}
                
                clip.metadata[parent_key][sub_key] = value
            else:
                clip.metadata[key] = value
    
    return clip


def create_track_from_json(json_track: Dict[str, Any]) -> otio.schema.Track:
    """
    Create an OTIO track from JSON track data.
    
    Args:
        json_track: JSON track data from otio2json format
        
    Returns:
        OTIO Track object
    """
    # Create track with proper kind
    track_kind = json_track.get("kind", "Video")
    if track_kind.lower() == "video":
        track = otio.schema.Track(name=json_track.get("name", "Track"), kind=otio.schema.TrackKind.Video)
    elif track_kind.lower() == "audio":
        track = otio.schema.Track(name=json_track.get("name", "Track"), kind=otio.schema.TrackKind.Audio)
    else:
        track = otio.schema.Track(name=json_track.get("name", "Track"))
    
    # Add clips to track
    for json_clip in json_track.get("clips", []):
        if json_clip.get("type") == "gap":
            # Create gap
            duration_frames = json_clip.get("source_range", {}).get("duration_frames", 0)
            if duration_frames > 0:
                # Use fps from first real clip or default to 25
                fps = 25.0
                for clip_data in json_track.get("clips", []):
                    if clip_data.get("type") != "gap" and "source_range" in clip_data:
                        fps = clip_data["source_range"].get("fps", 25.0)
                        break
                
                duration = otio.opentime.RationalTime(duration_frames, fps)
                gap = otio.schema.Gap(
                    name=json_clip.get("name", "Gap"),
                    source_range=otio.opentime.TimeRange(duration=duration)
                )
                track.append(gap)
        else:
            # Create regular clip
            clip = create_clip_from_json(json_clip)
            track.append(clip)
    
    # Set track metadata
    if "metadata" in json_track and json_track["metadata"]:
        for key, value in json_track["metadata"].items():
            track.metadata[key] = value
    
    return track


def create_audio_clip_from_video_clip(video_clip_json: Dict[str, Any], link_group_id: int) -> Dict[str, Any]:
    """
    Create an audio clip JSON from a video clip JSON.
    
    Args:
        video_clip_json: Video clip JSON data
        link_group_id: Link group ID for linking video and audio
        
    Returns:
        Audio clip JSON data
    """
    # Copy the video clip data
    audio_clip = video_clip_json.copy()
    
    # Add audio-specific metadata
    if "metadata" not in audio_clip:
        audio_clip["metadata"] = {}
    
    # Add audio channel information (stereo by default)
    audio_clip["metadata"]["Resolve_OTIO_Channels"] = "[{'Source Channel ID': 0, 'Source Track ID': 0}, {'Source Channel ID': 1, 'Source Track ID': 0}]"
    audio_clip["metadata"]["Resolve_OTIO_Link Group ID"] = link_group_id
    
    return audio_clip


def create_matching_audio_track(video_track_json: Dict[str, Any], track_index: int) -> Dict[str, Any]:
    """
    Create a matching audio track from a video track.
    
    Args:
        video_track_json: Video track JSON data
        track_index: Index for the new audio track
        
    Returns:
        Audio track JSON data
    """
    # Create audio track structure
    audio_track = {
        "track_index": track_index,
        "name": "Audio 1",  # Standard audio track name
        "kind": "Audio",
        "clips": [],
        "metadata": {
            "Resolve_OTIO": {
                "Audio Type": "Stereo",
                "Locked": False,
                "SoloOn": False
            }
        }
    }
    
    # Create matching audio clips for each video clip
    for i, video_clip in enumerate(video_track_json.get("clips", [])):
        # Only create audio clips for video clips that reference actual media files
        if video_clip.get("type") != "gap" and "media_reference" in video_clip:
            media_ref = video_clip["media_reference"]
            target_url = media_ref.get("target_url", "")
            
            # Check if this looks like a video file that would have audio
            video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.mxf', '.mts', '.m2ts']
            has_audio = any(target_url.lower().endswith(ext) for ext in video_extensions)
            
            if has_audio:
                # Create audio clip with link group ID
                link_group_id = video_clip.get("metadata", {}).get("Resolve_OTIO_Link Group ID", i + 1)
                audio_clip = create_audio_clip_from_video_clip(video_clip, link_group_id)
                audio_track["clips"].append(audio_clip)
    
    return audio_track


def auto_generate_audio_tracks(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Automatically generate matching audio tracks for video tracks if none exist.
    
    Args:
        json_data: Original JSON data
        
    Returns:
        Enhanced JSON data with audio tracks
    """
    tracks = json_data.get("tracks", [])
    
    # Check if we have any audio tracks
    has_audio_tracks = any(track.get("kind", "").lower() == "audio" for track in tracks)
    
    if has_audio_tracks:
        # Audio tracks already exist, return as-is
        return json_data
    
    # Find video tracks that should have matching audio
    video_tracks = [track for track in tracks if track.get("kind", "").lower() == "video"]
    
    if not video_tracks:
        # No video tracks found, return as-is
        return json_data
    
    print("✓ No audio tracks detected - automatically generating matching audio tracks")
    
    # Create enhanced JSON data
    enhanced_data = json_data.copy()
    enhanced_tracks = tracks.copy()
    
    # Generate audio tracks for each video track
    next_track_index = max([track.get("track_index", 0) for track in tracks]) + 1
    
    for video_track in video_tracks:
        # Check if this video track has clips with media files
        has_media_clips = any(
            clip.get("type") != "gap" and "media_reference" in clip 
            for clip in video_track.get("clips", [])
        )
        
        if has_media_clips:
            audio_track = create_matching_audio_track(video_track, next_track_index)
            enhanced_tracks.append(audio_track)
            
            print(f"  - Created audio track '{audio_track['name']}' matching video track '{video_track.get('name', 'Unknown')}'")
            print(f"    • {len(audio_track['clips'])} audio clips generated")
            
            next_track_index += 1
    
    # Update the tracks and summary
    enhanced_data["tracks"] = enhanced_tracks
    
    # Update summary if it exists
    if "summary" in enhanced_data:
        original_tracks = enhanced_data["summary"].get("total_tracks", len(tracks))
        total_audio_clips = sum(len(track["clips"]) for track in enhanced_tracks if track.get("kind", "").lower() == "audio")
        
        enhanced_data["summary"]["total_tracks"] = len(enhanced_tracks)
        enhanced_data["summary"]["total_clips"] = enhanced_data["summary"].get("total_clips", 0) + total_audio_clips
    
    return enhanced_data


def create_timeline_from_json(json_data: Dict[str, Any]) -> otio.schema.Timeline:
    """
    Create an OTIO timeline from JSON data.
    Automatically generates matching audio tracks if only video tracks are present.
    
    Args:
        json_data: JSON data from otio2json format
        
    Returns:
        OTIO Timeline object
    """
    # Auto-generate audio tracks if needed
    enhanced_data = auto_generate_audio_tracks(json_data)
    
    # Extract timeline info
    timeline_info = enhanced_data.get("timeline", {})
    timeline_name = timeline_info.get("name", "Timeline")
    timeline_fps = timeline_info.get("fps", 25.0)
    
    # Create timeline
    timeline = otio.schema.Timeline(name=timeline_name)
    
    # Set timeline metadata
    if "metadata" in timeline_info and timeline_info["metadata"]:
        for key, value in timeline_info["metadata"].items():
            timeline.metadata[key] = value
    
    # Add tracks to timeline
    for json_track in enhanced_data.get("tracks", []):
        track = create_track_from_json(json_track)
        timeline.tracks.append(track)
    
    return timeline


def convert_json_to_otio(json_filepath: str, output_filepath: str = None) -> bool:
    """
    Convert JSON to OTIO by rebuilding the timeline structure.
    
    Args:
        json_filepath: Path to JSON file
        output_filepath: Output OTIO file path (optional)
        
    Returns:
        True if successful
    """
    try:
        # Load JSON data
        with open(json_filepath, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        print(f"✓ Loaded JSON: {json_filepath}")
        
        # Validate JSON format
        required_fields = ["timeline", "tracks", "summary"]
        for field in required_fields:
            if field not in json_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Check if timeline name is missing and add from project data
        if not json_data.get("timeline", {}).get("name"):
            project_data = load_project_data()
            project_title = project_data.get("projectTitle", "Timeline")
            if "timeline" not in json_data:
                json_data["timeline"] = {}
            json_data["timeline"]["name"] = project_title
            print(f"✓ Added timeline name from project data: {project_title}")
        
        # Create timeline from JSON
        timeline = create_timeline_from_json(json_data)
        print(f"✓ Created timeline: {timeline.name}")
        
        # Determine output path
        if not output_filepath:
            json_name = Path(json_filepath).stem
            output_dir = Path(json_filepath).parent
            output_filepath = output_dir / f"{json_name}.otio"
        
        # Write timeline to file
        otio.adapters.write_to_file(timeline, str(output_filepath))
        print(f"✓ Wrote OTIO file: {output_filepath}")
        
        # Print summary
        summary = json_data.get("summary", {})
        print(f"  - Tracks: {summary.get('total_tracks', 'unknown')}")
        print(f"  - Clips: {summary.get('total_clips', 'unknown')}")
        print(f"  - Duration: {summary.get('timeline_duration_frames', 'unknown')} frames")
        
        return True
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        import traceback
        traceback.print_exc()
        return False


def apply_json_edits_to_timeline() -> bool:
    """
    Hands-off conversion: automatically find JSON in timeline_edited and convert to OTIO.
    
    Returns:
        True if successful
    """
    try:
        # Define paths relative to script location
        script_dir = Path(__file__).parent.resolve()
        project_root = script_dir.parent.parent
        timeline_edited_dir = project_root / "data" / "timelineprocessing" / "timeline_edited"
        
        # Ensure timeline_edited directory exists
        timeline_edited_dir.mkdir(parents=True, exist_ok=True)
        
        # Find JSON file in timeline_edited directory
        json_files = list(timeline_edited_dir.glob("*.json"))
        
        if not json_files:
            print(f"ERROR: No JSON files found in {timeline_edited_dir}")
            print("Please copy/move your edited JSON file to the timeline_edited directory")
            return False
        
        if len(json_files) > 1:
            print(f"WARNING: Multiple JSON files found in {timeline_edited_dir}:")
            for f in json_files:
                print(f"  - {f.name}")
            print("Using the first one found...")
        
        json_file = json_files[0]
        output_file = timeline_edited_dir / json_file.with_suffix('.otio').name
        
        print(f"✓ Found edited JSON: {json_file.name}")
        print(f"✓ Output will be: {output_file.name}")
        print()
        
        # Check if output exists
        if output_file.exists():
            print(f"Overwriting existing file: {output_file}")
        
        # Perform conversion
        print("Rebuilding OTIO from JSON data...")
        success = convert_json_to_otio(str(json_file), str(output_file))
        
        if success:
            print(f"✓ Created modified timeline: {output_file}")
            print("You can now import this OTIO back into DaVinci Resolve")
        
        return success
        
    except Exception as e:
        print(f"Error: {e}")
        return False


# Adapter metadata
__version__ = "1.0.0"
__author__ = "NiceTouch"
__description__ = "JSON to OTIO adapter - rebuild timelines from JSON"


if __name__ == "__main__":
    print("=== JSON to OTIO Converter (Rebuild) ===")
    print("Rebuilding OTIO timeline from JSON data")
    print()
    
    success = apply_json_edits_to_timeline()
    
    if success:
        print("\n=== Conversion completed successfully! ===")
        sys.exit(0)
    else:
        print("\n=== Conversion failed! ===")
        sys.exit(1)
