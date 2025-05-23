#!/usr/bin/env python3
"""
Interactive wrapper for VideoAnalyzer.

This script provides a user-friendly console interface for processing videos
with the VideoAnalyzer tool, including enhanced accuracy features like
project brief integration and silence detection.
"""

import os
import sys
import json
from pathlib import Path

# Add the current directory to the path so we can import videoanalyzer
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from videoanalyzer import VideoAnalyzer


def get_user_input():
    """Get all required inputs from the user via console prompts."""
    print("=" * 60)
    print("VideoAnalyzer - Interactive Video Transcription Tool")
    print("=" * 60)
    print()
    
    inputs = {}
    
    # Video file path (required)
    while True:
        video_path = input("Enter video file path: ").strip()
        if not video_path:
            print("❌ Video file path is required!")
            continue
        
        # Handle quotes around path
        video_path = video_path.strip('"\'')
        
        if not os.path.isfile(video_path):
            print(f"❌ Video file not found: {video_path}")
            continue
        
        inputs['video_path'] = video_path
        break
    
    # Output file path (optional)
    output_path = input("Enter output file path (press Enter for auto): ").strip()
    if output_path:
        output_path = output_path.strip('"\'')
        inputs['output_path'] = output_path
    else:
        inputs['output_path'] = None
    
    # Project brief file (optional)
    brief_path = input("Enter project brief file path (press Enter to skip): ").strip()
    if brief_path:
        brief_path = brief_path.strip('"\'')
        if os.path.isfile(brief_path):
            inputs['brief_path'] = brief_path
            print(f"✅ Brief file found: {brief_path}")
        else:
            print(f"⚠️  Brief file not found: {brief_path} - continuing without brief")
            inputs['brief_path'] = None
    else:
        inputs['brief_path'] = None
    
    # Custom spelling file (optional)
    custom_spell_path = input("Enter custom spelling file path (press Enter to skip): ").strip()
    if custom_spell_path:
        custom_spell_path = custom_spell_path.strip('"\'')
        if os.path.isfile(custom_spell_path):
            try:
                with open(custom_spell_path, 'r') as f:
                    inputs['custom_spell'] = json.load(f)
                print(f"✅ Custom spelling file loaded: {custom_spell_path}")
            except Exception as e:
                print(f"⚠️  Error loading custom spelling file: {e} - continuing without custom spelling")
                inputs['custom_spell'] = None
        else:
            print(f"⚠️  Custom spelling file not found: {custom_spell_path} - continuing without custom spelling")
            inputs['custom_spell'] = None
    else:
        inputs['custom_spell'] = None
    
    # Silence threshold (optional)
    while True:
        silence_input = input("Enter silence threshold in milliseconds (press Enter for 1000ms): ").strip()
        if not silence_input:
            inputs['silence_threshold_ms'] = 1000
            break
        
        try:
            threshold = int(silence_input)
            if threshold < 100:
                print("❌ Silence threshold must be at least 100ms")
                continue
            if threshold > 10000:
                print("❌ Silence threshold should not exceed 10000ms (10 seconds)")
                continue
            inputs['silence_threshold_ms'] = threshold
            break
        except ValueError:
            print("❌ Please enter a valid number")
            continue
    
    return inputs


def display_summary(inputs):
    """Display a summary of the processing configuration."""
    print("\n" + "=" * 60)
    print("PROCESSING CONFIGURATION")
    print("=" * 60)
    print(f"📹 Video File: {inputs['video_path']}")
    
    if inputs['output_path']:
        print(f"💾 Output File: {inputs['output_path']}")
    else:
        auto_output = f"{inputs['video_path']}.transcript.json"
        print(f"💾 Output File: {auto_output} (auto-generated)")
    
    if inputs['brief_path']:
        print(f"📋 Project Brief: {inputs['brief_path']}")
    else:
        print("📋 Project Brief: None")
    
    if inputs['custom_spell']:
        spell_count = len(inputs['custom_spell'])
        print(f"📝 Custom Spellings: {spell_count} entries")
    else:
        print("📝 Custom Spellings: None")
    
    print(f"🔇 Silence Threshold: {inputs['silence_threshold_ms']}ms")
    print("=" * 60)


def main():
    """Main interactive function."""
    try:
        # Get user inputs
        inputs = get_user_input()
        
        # Display configuration summary
        display_summary(inputs)
        
        # Confirm before processing
        print("\nReady to process video...")
        confirm = input("Continue? (Y/n): ").strip().lower()
        if confirm and confirm not in ['y', 'yes']:
            print("❌ Processing cancelled by user")
            return
        
        print("\n🚀 Starting video analysis...")
        print("=" * 60)
        
        # Initialize VideoAnalyzer
        analyzer = VideoAnalyzer(brief_path=inputs['brief_path'])
        
        # Process the video
        result = analyzer.analyze(
            video_path=inputs['video_path'],
            output_path=inputs['output_path'],
            custom_spell=inputs['custom_spell'],
            brief_path=inputs['brief_path'],
            silence_threshold_ms=inputs['silence_threshold_ms']
        )
        
        # Check for errors
        if "error" in result:
            print(f"❌ Processing failed: {result['error']}")
            return
        
        # Display success summary
        print("\n✅ Video analysis completed successfully!")
        print("=" * 60)
        print("RESULTS SUMMARY")
        print("=" * 60)
        print(f"📹 File: {result['file_name']}")
        print(f"🎬 FPS: {result['fps']}")
        print(f"⏱️  Duration: {result['duration_frames']} frames")
        print(f"🎤 Speakers: {', '.join(result['speakers'])}")
        print(f"📝 Words: {len([w for w in result['words'] if w['word'] != '**SILENCE**'])}")
        
        silence_count = len([w for w in result['words'] if w['word'] == '**SILENCE**'])
        print(f"🔇 Silence Periods: {silence_count}")
        
        # Determine output file path
        output_file = inputs['output_path'] or f"{inputs['video_path']}.transcript.json"
        print(f"💾 Saved to: {output_file}")
        
        print("\n🎉 Ready for editing workflow!")
        
    except KeyboardInterrupt:
        print("\n❌ Processing interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please check your inputs and try again.")


if __name__ == "__main__":
    main()
