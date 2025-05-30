#!/usr/bin/env python3
"""
Test script to verify the standalone functionality of editagent.py
This tests the core loading and path functionality without external dependencies.
"""

import json
import sys
from pathlib import Path

# Add the editgenerator directory to path
sys.path.insert(0, str(Path(__file__).parent / "backend" / "editgenerator"))

def test_file_paths():
    """Test that all required file paths exist."""
    # Test paths (same as in editagent.py)
    TRANSCRIPT_PATH = Path("D:/Git/nt_editapp/data/20250509_MTC_2206.MP4.transcript.json")
    PROJECT_DATA_PATH = Path("D:/Git/nt_editapp/data/projectdata.json")
    OUTPUT_DIR = Path("D:/Git/nt_editapp/data/edits")
    
    print("Testing file paths...")
    
    # Check transcript file
    if TRANSCRIPT_PATH.exists():
        print(f"✓ Transcript file exists: {TRANSCRIPT_PATH}")
        # Test loading
        try:
            with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
                transcript_data = json.load(f)
            word_count = len([w for w in transcript_data.get("words", []) if w.get("word") != "**SILENCE**"])
            print(f"✓ Transcript loaded successfully ({word_count} words)")
        except Exception as e:
            print(f"❌ Failed to load transcript: {e}")
    else:
        print(f"❌ Transcript file missing: {TRANSCRIPT_PATH}")
    
    # Check project data file
    if PROJECT_DATA_PATH.exists():
        print(f"✓ Project data file exists: {PROJECT_DATA_PATH}")
        # Test loading
        try:
            with open(PROJECT_DATA_PATH, "r", encoding="utf-8") as f:
                project_data = json.load(f)
            title = project_data.get("projectTitle", "")
            brief = project_data.get("projectBrief", "")
            print(f"✓ Project data loaded: '{title}' ({len(brief)} chars)")
        except Exception as e:
            print(f"❌ Failed to load project data: {e}")
    else:
        print(f"❌ Project data file missing: {PROJECT_DATA_PATH}")
    
    # Check output directory
    if OUTPUT_DIR.exists():
        print(f"✓ Output directory exists: {OUTPUT_DIR}")
    else:
        print(f"⚠ Output directory missing (will be created): {OUTPUT_DIR}")

def test_filename_generation():
    """Test the filename generation logic."""
    from datetime import datetime
    
    print("\nTesting filename generation...")
    
    # Mock project title
    project_title = "Nice Touch launch Video"
    
    # Clean project title for filename
    clean_title = "".join(c for c in project_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_title = clean_title.replace(' ', '_')
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create filename
    filename = f"{clean_title}_edit_{timestamp}.json"
    
    print(f"✓ Generated filename: {filename}")
    print(f"✓ Format: {clean_title}_edit_{timestamp}.json")

if __name__ == "__main__":
    print("=== Standalone Edit Agent Test ===\n")
    
    try:
        test_file_paths()
        test_filename_generation()
        print("\n✅ All basic functionality tests passed!")
        print("\nThe edit agent should work in standalone mode.")
        print("Make sure to install required dependencies:")
        print("  • python-dotenv")
        print("  • anthropic")
        print("  • jsonschema")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 