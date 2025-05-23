#!/usr/bin/env python3

"""
Interactive wrapper for EditAgent.

This script provides a user-friendly console interface for processing video transcripts
with the EditAgent tool, including transcript quality analysis and AI-powered editing
with confidence score integration.
"""

import os
import sys
import json
from pathlib import Path

# Add the current directory to the path so we can import editagent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from editagent import process_transcript, analyze_transcript_quality, stream_to_console


def get_user_input():
    """Get all required inputs from the user via console prompts."""
    print("=" * 60)
    print("EditAgent - Interactive Video Transcript Editor")
    print("=" * 60)
    print()
    
    # Get transcript file path
    while True:
        transcript_path = input("📁 Enter the path to your transcript JSON file: ").strip().strip('"')
        
        if not transcript_path:
            print("❌ Please provide a transcript file path.")
            continue
            
        # Convert to Path object and resolve
        transcript_file = Path(transcript_path)
        
        if not transcript_file.exists():
            print(f"❌ File not found: {transcript_file}")
            continue
            
        if not transcript_file.suffix.lower() == '.json':
            print("❌ Please provide a JSON file.")
            continue
            
        break
    
    # Get project brief
    print("\n📝 Project Brief Options:")
    print("  1. Use default brief (projectbrieftemp.txt)")
    print("  2. Enter custom brief text")
    print("  3. Load brief from file")
    
    while True:
        brief_choice = input("\nSelect brief option (1-3): ").strip()
        
        if brief_choice == "1":
            # Use default brief
            brief_path = Path(__file__).parent / "prompts" / "projectbrieftemp.txt"
            try:
                with open(brief_path, "r", encoding="utf-8") as f:
                    user_brief = f.read()
                print(f"✓ Using default brief from: {brief_path}")
                break
            except FileNotFoundError:
                print(f"❌ Default brief file not found: {brief_path}")
                continue
                
        elif brief_choice == "2":
            # Custom brief text
            print("\n📝 Enter your project brief (press Enter twice when done):")
            brief_lines = []
            empty_lines = 0
            
            while empty_lines < 2:
                line = input()
                if line.strip() == "":
                    empty_lines += 1
                else:
                    empty_lines = 0
                brief_lines.append(line)
            
            user_brief = "\n".join(brief_lines[:-2])  # Remove the two empty lines at the end
            
            if user_brief.strip():
                print("✓ Custom brief entered successfully")
                break
            else:
                print("❌ Brief cannot be empty")
                continue
                
        elif brief_choice == "3":
            # Load from file
            brief_file_path = input("📁 Enter path to brief file: ").strip().strip('"')
            brief_file = Path(brief_file_path)
            
            if not brief_file.exists():
                print(f"❌ Brief file not found: {brief_file}")
                continue
                
            try:
                with open(brief_file, "r", encoding="utf-8") as f:
                    user_brief = f.read()
                print(f"✓ Brief loaded from: {brief_file}")
                break
            except Exception as e:
                print(f"❌ Error reading brief file: {e}")
                continue
        else:
            print("❌ Please select 1, 2, or 3")
            continue
    
    # Get project name (optional)
    project_name = input(f"\n🏷️  Project name (default: 'Video Edit'): ").strip()
    if not project_name:
        project_name = "Video Edit"
    
    # Get output options
    print(f"\n💾 Output Options:")
    print(f"  1. Auto-generate filename in edits folder")
    print(f"  2. Specify custom output path")
    
    while True:
        output_choice = input("Select output option (1-2): ").strip()
        
        if output_choice == "1":
            # Auto-generate
            output_dir = Path(__file__).parent / "edits"
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / f"{project_name.replace(' ', '_')}.edited.json"
            break
            
        elif output_choice == "2":
            # Custom path
            custom_output = input("📁 Enter output file path: ").strip().strip('"')
            output_path = Path(custom_output)
            
            # Create directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            break
        else:
            print("❌ Please select 1 or 2")
            continue
    
    return {
        "transcript_file": transcript_file,
        "user_brief": user_brief,
        "project_name": project_name,
        "output_path": output_path
    }


def print_summary(config):
    """Print a summary of the configuration before processing."""
    print("\n" + "=" * 60)
    print("PROCESSING SUMMARY")
    print("=" * 60)
    print(f"📁 Transcript file: {config['transcript_file']}")
    print(f"🏷️  Project name: {config['project_name']}")
    print(f"💾 Output file: {config['output_path']}")
    print(f"📝 Brief preview: {config['user_brief'][:150]}...")
    print("=" * 60)


def main():
    """Main interactive function."""
    try:
        # Get user inputs
        config = get_user_input()
        
        # Print summary
        print_summary(config)
        
        # Confirm before processing
        confirm = input("\n🚀 Ready to process? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Processing cancelled.")
            return
        
        # Load transcript data
        print(f"\n📖 Loading transcript from: {config['transcript_file']}")
        try:
            with open(config['transcript_file'], "r", encoding="utf-8") as f:
                transcript_data = json.load(f)
            print("✓ Transcript loaded successfully")
        except Exception as e:
            print(f"❌ Error loading transcript: {e}")
            return
        
        # Analyze transcript quality
        print("\n🔍 Analyzing transcript quality...")
        quality_report = analyze_transcript_quality(transcript_data)
        
        if "error" not in quality_report and "warning" not in quality_report:
            print(f"✓ Transcript Quality Report:")
            print(f"  • Total words: {quality_report['total_words']}")
            print(f"  • Average confidence: {quality_report['avg_confidence']}")
            print(f"  • Low confidence words: {quality_report['low_confidence_words']} ({quality_report['low_confidence_percentage']}%)")
            
            if quality_report['worst_words']:
                print(f"  • Words needing attention: {len(quality_report['worst_words'])} words with confidence < 0.7")
                if quality_report['avg_confidence'] < 0.8:
                    print("  ⚠️ Consider reviewing audio quality or manual transcript verification")
            
            print(f"  • Speaker confidence:")
            for speaker, conf in quality_report['speaker_confidence'].items():
                status = "✓" if conf >= 0.8 else "⚠️" if conf >= 0.7 else "❌"
                print(f"    {status} {speaker}: {conf}")
        
        # Process with EditAgent
        print(f"\n🤖 Starting EditAgent processing...")
        print(f"💭 AI thinking and response will be displayed below:")
        print("-" * 60)
        
        result = process_transcript(
            transcript_data, 
            config['user_brief'], 
            output_filename=str(config['output_path']),
            streaming_callback=stream_to_console
        )
        
        print("-" * 60)
        print("🎉 Processing complete!")
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return
        
        # Success summary
        print(f"✓ Generated {len(result['segments'])} segments")
        print(f"✓ Target duration: {result['target_duration_frames']} frames")
        print(f"✓ Actual duration: {result['actual_duration_frames']} frames")
        print(f"✓ Output saved to: {config['output_path']}")
        
        # Analyze confidence in the generated segments
        if 'segments' in result:
            segment_confidences = [seg.get('avg_confidence', 0) for seg in result['segments'] if seg.get('avg_confidence')]
            if segment_confidences:
                avg_segment_confidence = sum(segment_confidences) / len(segment_confidences)
                print(f"✓ Average segment confidence: {avg_segment_confidence:.3f}")
                
                low_conf_segments = [i for i, seg in enumerate(result['segments']) 
                                   if seg.get('avg_confidence', 1) < 0.7]
                if low_conf_segments:
                    print(f"⚠️ Segments with low confidence: {len(low_conf_segments)} (review recommended)")
        
        # Offer to show detailed results
        show_details = input(f"\n📊 Show detailed segment breakdown? (y/N): ").strip().lower()
        if show_details in ['y', 'yes']:
            print(f"\n📋 SEGMENT BREAKDOWN:")
            print("-" * 80)
            for i, segment in enumerate(result['segments'][:5], 1):  # Show first 5 segments
                conf_str = f" (conf: {segment.get('avg_confidence', 'N/A'):.3f})" if segment.get('avg_confidence') else ""
                print(f"{i}. {segment['speaker']}: \"{segment['text'][:60]}...\" [{segment['frame_in']}-{segment['frame_out']}]{conf_str}")
            
            if len(result['segments']) > 5:
                print(f"... and {len(result['segments']) - 5} more segments")
        
        print(f"\n🎬 Edit file ready at: {config['output_path']}")
        
    except KeyboardInterrupt:
        print(f"\n\n❌ Process interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
