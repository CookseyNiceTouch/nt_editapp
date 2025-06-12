#!/usr/bin/env python3
"""
Test script for the crop tool functionality.
"""

import sys
import os
from pathlib import Path

# Add the editgenerator directory to the path
script_dir = Path(__file__).parent.resolve()
editgenerator_dir = script_dir / "backend" / "editgenerator"
sys.path.insert(0, str(editgenerator_dir))

from toolcalling.toolcaller import tool_caller

def test_crop_tool():
    """Test the crop tool functionality."""
    
    print("=== Testing Crop Tool ===")
    
    # Test 1: Basic connection test
    print("\n1. Testing DaVinci Resolve connection...")
    connection_result = tool_caller.call_tool("test_resolve_connection")
    print(f"Connection result: {connection_result}")
    
    if not connection_result.get("success") or not connection_result.get("result", {}).get("connected"):
        print("❌ DaVinci Resolve not connected. Cannot test crop tool.")
        return False
    
    # Test 2: List clips to see what's available
    print("\n2. Listing clips in timeline...")
    clips_result = tool_caller.call_tool("list_clips_in_tracks")
    print(f"Clips result: {clips_result}")
    
    if not clips_result.get("success"):
        print("❌ Could not list clips")
        return False
    
    # Test 3: Apply crop to first clip if available
    timeline_data = clips_result.get("result", {})
    tracks = timeline_data.get("tracks", [])
    
    if not tracks or not tracks[0].get("clips"):
        print("❌ No clips found to test crop on")
        return False
    
    print(f"\n3. Applying crop to first clip...")
    crop_result = tool_caller.call_tool("apply_crop_to_clip", {
        "track_index": 1,
        "clip_index": 1,
        "crop_left": 0.1,
        "crop_right": 0.1,
        "crop_top": 0.05,
        "crop_bottom": 0.05,
        "description": "Test crop"
    })
    
    print(f"Crop result: {crop_result}")
    
    if crop_result.get("success"):
        print("✅ Crop tool test successful!")
        return True
    else:
        print("❌ Crop tool test failed!")
        return False

if __name__ == "__main__":
    success = test_crop_tool()
    sys.exit(0 if success else 1) 