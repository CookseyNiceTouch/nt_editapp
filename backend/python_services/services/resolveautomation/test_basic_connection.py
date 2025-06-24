#!/usr/bin/env python3
"""
DaVinci Resolve Basic Connection Test Script
============================================

This script tests the fundamental connection to DaVinci Resolve following
the official Blackmagic Design documentation requirements.

Based on: https://resolvedevdoc.readthedocs.io/en/latest/readme_resolveapi.html

Prerequisites:
- DaVinci Resolve installed and running
- External scripting enabled in Resolve Preferences
- Proper environment variables set (handled automatically by this script)
"""

import sys
import os
import platform
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def setup_environment_variables():
    """Set up required environment variables for DaVinci Resolve API"""
    print("=== Environment Variables Setup ===")
    
    # Get current script directory
    current_dir = Path(__file__).parent.absolute()
    lib_dir = current_dir / 'lib'
    
    # Platform-specific paths according to official documentation
    system = platform.system()
    
    if system == "Windows":
        # Windows paths from official docs
        api_path = os.path.expandvars(r"%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting")
        lib_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
        local_lib_path = lib_dir / "fusionscript.dll"
        
        print(f"Platform: Windows")
        print(f"Expected system DLL: {lib_path}")
        print(f"Local DLL: {local_lib_path}")
        
        # Use local DLL if it exists, otherwise system DLL
        if local_lib_path.exists():
            os.environ['RESOLVE_SCRIPT_LIB'] = str(local_lib_path)
            print(f"✓ Using local fusionscript.dll")
        elif os.path.exists(lib_path):
            os.environ['RESOLVE_SCRIPT_LIB'] = lib_path
            print(f"✓ Using system fusionscript.dll")
        else:
            print(f"✗ fusionscript.dll not found in either location")
            return False
            
    elif system == "Darwin":  # macOS
        api_path = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
        lib_path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
        os.environ['RESOLVE_SCRIPT_LIB'] = lib_path
        print(f"Platform: macOS")
        
    elif system == "Linux":
        # Linux paths (may vary by installation)
        api_path = "/opt/resolve/Developer/Scripting"
        lib_path = "/opt/resolve/libs/Fusion/fusionscript.so"
        
        # Alternative path for some installations
        if not os.path.exists(api_path):
            api_path = "/home/resolve/Developer/Scripting"
            lib_path = "/home/resolve/libs/Fusion/fusionscript.so"
            
        os.environ['RESOLVE_SCRIPT_LIB'] = lib_path
        print(f"Platform: Linux")
        
    else:
        print(f"✗ Unsupported platform: {system}")
        return False
    
    # Set API path and Python path
    os.environ['RESOLVE_SCRIPT_API'] = api_path
    
    # Update PYTHONPATH to include Modules directory
    modules_path = os.path.join(api_path, "Modules")
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    
    if modules_path not in current_pythonpath:
        if current_pythonpath:
            os.environ['PYTHONPATH'] = f"{current_pythonpath}{os.pathsep}{modules_path}"
        else:
            os.environ['PYTHONPATH'] = modules_path
    
    # Also add to sys.path for this session
    if modules_path not in sys.path:
        sys.path.insert(0, modules_path)
    
    # Add local lib directory to path
    if str(lib_dir) not in sys.path:
        sys.path.insert(0, str(lib_dir))
    
    # Print environment setup
    print(f"RESOLVE_SCRIPT_API: {os.environ.get('RESOLVE_SCRIPT_API', 'NOT SET')}")
    print(f"RESOLVE_SCRIPT_LIB: {os.environ.get('RESOLVE_SCRIPT_LIB', 'NOT SET')}")
    print(f"PYTHONPATH includes: {modules_path}")
    
    # Verify paths exist
    api_exists = os.path.exists(api_path)
    lib_exists = os.path.exists(os.environ.get('RESOLVE_SCRIPT_LIB', ''))
    modules_exists = os.path.exists(modules_path)
    
    print(f"API path exists: {api_exists}")
    print(f"Library path exists: {lib_exists}")
    print(f"Modules path exists: {modules_exists}")
    
    if not lib_exists:
        print("⚠️  WARNING: fusionscript library not found")
        print("   This may indicate DaVinci Resolve is not installed")
        print("   or installation is incomplete")
    
    return True

def test_resolve_connection():
    """Test the actual connection to DaVinci Resolve"""
    print("\n=== DaVinci Resolve Connection Test ===")
    
    try:
        # Try to import DaVinciResolveScript
        print("Attempting to import DaVinciResolveScript...")
        import DaVinciResolveScript as dvr_script
        print("✓ Successfully imported DaVinciResolveScript")
        
        # Try to connect to Resolve
        print("Attempting to connect to DaVinci Resolve...")
        resolve = dvr_script.scriptapp('Resolve')
        
        if resolve:
            print("✓ Successfully connected to DaVinci Resolve!")
            
            # Get version info
            try:
                version = resolve.GetVersionString()
                product = resolve.GetProductName()
                print(f"✓ Connected to: {product} v{version}")
            except Exception as e:
                print(f"⚠️  Could not get version info: {e}")
            
            # Test ProjectManager and get detailed project info
            try:
                project_manager = resolve.GetProjectManager()
                if project_manager:
                    print("✓ Successfully got ProjectManager")
                    
                    # Get current database info
                    try:
                        db_info = project_manager.GetCurrentDatabase()
                        print(f"✓ Current database: {db_info.get('DbName', 'Unknown')} ({db_info.get('DbType', 'Unknown')})")
                    except Exception as e:
                        print(f"⚠️  Could not get database info: {e}")
                    
                    # Get current project
                    current_project = project_manager.GetCurrentProject()
                    if current_project:
                        project_name = current_project.GetName()
                        project_id = current_project.GetUniqueId()
                        print(f"✓ Current project: '{project_name}' (ID: {project_id[:8]}...)")
                        
                        # Get project details
                        timeline_count = current_project.GetTimelineCount()
                        print(f"✓ Project has {timeline_count} timeline(s)")
                        
                        # List all timelines
                        if timeline_count > 0:
                            print("  📽️  Timelines in project:")
                            for i in range(1, timeline_count + 1):
                                try:
                                    timeline = current_project.GetTimelineByIndex(i)
                                    if timeline:
                                        tl_name = timeline.GetName()
                                        tl_start = timeline.GetStartFrame()
                                        tl_end = timeline.GetEndFrame()
                                        duration = tl_end - tl_start
                                        video_tracks = timeline.GetTrackCount("video")
                                        audio_tracks = timeline.GetTrackCount("audio")
                                        print(f"    {i}. '{tl_name}' - {duration} frames ({tl_start}-{tl_end})")
                                        print(f"       📹 {video_tracks} video tracks, 🔊 {audio_tracks} audio tracks")
                                except Exception as e:
                                    print(f"    {i}. [Error getting timeline {i}: {e}]")
                        
                        # Get current timeline details
                        try:
                            current_timeline = current_project.GetCurrentTimeline()
                            if current_timeline:
                                current_tl_name = current_timeline.GetName()
                                print(f"✓ Current timeline: '{current_tl_name}'")
                                
                                # Get timeline details
                                start_tc = current_timeline.GetStartTimecode()
                                current_tc = current_timeline.GetCurrentTimecode()
                                print(f"  ⏰ Start timecode: {start_tc}")
                                print(f"  ⏰ Current timecode: {current_tc}")
                                
                            else:
                                print("! No timeline currently selected")
                        except Exception as e:
                            print(f"⚠️  Could not get current timeline info: {e}")
                        
                        # Get media pool info
                        try:
                            media_pool = current_project.GetMediaPool()
                            if media_pool:
                                print("✓ Successfully accessed Media Pool")
                                root_folder = media_pool.GetRootFolder()
                                if root_folder:
                                    clips = root_folder.GetClipList()
                                    clip_count = len(clips) if clips else 0
                                    print(f"  📁 Root folder has {clip_count} clip(s)")
                                    
                                    # Show first few clips
                                    if clips and clip_count > 0:
                                        print("  🎬 Sample clips:")
                                        for i, clip in enumerate(clips[:3]):  # Show first 3 clips
                                            try:
                                                clip_name = clip.GetName()
                                                clip_duration = clip.GetClipProperty("Duration")
                                                print(f"    - '{clip_name}' ({clip_duration})")
                                            except Exception as e:
                                                print(f"    - [Error getting clip info: {e}]")
                                        if clip_count > 3:
                                            print(f"    ... and {clip_count - 3} more")
                        except Exception as e:
                            print(f"⚠️  Could not access Media Pool: {e}")
                        
                        # Get some project settings
                        try:
                            timeline_frame_rate = current_project.GetSetting("timelineFrameRate")
                            video_format = current_project.GetSetting("timelineResolutionWidth")
                            video_height = current_project.GetSetting("timelineResolutionHeight")
                            print(f"✓ Project settings: {video_format}x{video_height} @ {timeline_frame_rate}")
                        except Exception as e:
                            print(f"⚠️  Could not get project settings: {e}")
                        
                    else:
                        print("! No current project loaded")
                        print("  To test properly, please:")
                        print("  1. Create or open a project in DaVinci Resolve")
                        print("  2. Add some media to the Media Pool")
                        print("  3. Create a timeline")
                        
                        # Show available projects
                        try:
                            project_list = project_manager.GetProjectListInCurrentFolder()
                            if project_list:
                                print(f"  📂 Available projects in current folder: {len(project_list)}")
                                for project in project_list[:5]:  # Show first 5
                                    print(f"    - {project}")
                                if len(project_list) > 5:
                                    print(f"    ... and {len(project_list) - 5} more")
                        except Exception as e:
                            print(f"⚠️  Could not list available projects: {e}")
                            
                else:
                    print("✗ Failed to get ProjectManager")
                    return False
            except Exception as e:
                print(f"✗ Error accessing ProjectManager: {e}")
                return False
                
            # Test MediaStorage
            try:
                media_storage = resolve.GetMediaStorage()
                if media_storage:
                    print("✓ Successfully got MediaStorage")
                else:
                    print("⚠️  Could not get MediaStorage")
            except Exception as e:
                print(f"⚠️  Error accessing MediaStorage: {e}")
            
            return True
            
        else:
            print("✗ Failed to connect to DaVinci Resolve")
            print("\nTroubleshooting checklist:")
            print("  1. ✓ DaVinci Resolve is running")
            print("  2. ✓ Go to DaVinci Resolve > Preferences > General")
            print("  3. ✓ Find 'External scripting using' option")
            print("  4. ✓ Set it to 'Local' (for same machine)")
            print("  5. ✓ Restart DaVinci Resolve after changing this setting")
            print("  6. ✓ Make sure no firewall is blocking the connection")
            return False
            
    except ImportError as e:
        print(f"✗ Import Error: {e}")
        print("\nThis usually means:")
        print("  1. fusionscript library is missing, corrupted, or incompatible")
        print("  2. DaVinci Resolve is not properly installed")
        print("  3. Python version compatibility issue")
        print("  4. Environment variables not set correctly")
        
        # Additional diagnostics
        if "'imp'" in str(e):
            print("\n🔴 CRITICAL: This error indicates Python 3.12+ compatibility issue!")
            print("   DaVinci Resolve's API uses the deprecated 'imp' module")
            print("   which was removed in Python 3.12")
            print("   Please use Python 3.6-3.11")
        
        return False
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        logger.exception("Full traceback:")
        return False

def main():
    """Main test function"""
    print("🎬 DaVinci Resolve API Connection Test")
    print("=" * 50)
    
    # Setup environment
    if not setup_environment_variables():
        print("\n❌ Test FAILED: Environment setup failed")
        return False
    
    # Test connection
    if not test_resolve_connection():
        print("\n❌ Test FAILED: Could not connect to DaVinci Resolve")
        return False
    
    print("\n✅ Test PASSED: DaVinci Resolve API is working correctly!")
    print("\nYour system is ready for DaVinci Resolve automation.")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 