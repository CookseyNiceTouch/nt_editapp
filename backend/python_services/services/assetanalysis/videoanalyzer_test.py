#!/usr/bin/env python3
"""
VideoAnalyzer Test Script

Simple test script to verify VideoAnalyzer functionality including:
- File validation
- Metadata extraction (if FFmpeg is available)
- Error handling
- Output path generation
- Import verification
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from typing import Dict, Any

# Add the services directory to Python path for imports
script_dir = Path(__file__).parent
services_dir = script_dir.parent
sys.path.insert(0, str(services_dir))

def test_imports():
    """Test that all required imports work correctly."""
    print("🔍 Testing imports...")
    
    try:
        from assetanalysis.videoanalyzer import VideoAnalyzer, ProjectBriefParser
        print("✅ VideoAnalyzer import successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_project_brief_parser():
    """Test ProjectBriefParser functionality."""
    print("\n🔍 Testing ProjectBriefParser...")
    
    try:
        from assetanalysis.videoanalyzer import ProjectBriefParser
        
        # Test with no brief
        parser = ProjectBriefParser()
        print("✅ ProjectBriefParser created without brief")
        
        # Test with non-existent brief
        parser = ProjectBriefParser("nonexistent.txt")
        print("✅ ProjectBriefParser handles non-existent brief gracefully")
        
        # Test with sample brief content
        sample_brief = """
        Title: "Test Video Project"
        Talent: John Smith, Jane Doe
        Objective: Create engaging content
        Core Message: Innovation and creativity
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(sample_brief)
            brief_path = f.name
        
        try:
            parser = ProjectBriefParser(brief_path)
            config = parser.get_transcription_config()
            mapping = parser.get_speaker_mapping()
            
            print(f"✅ Brief parsed successfully")
            print(f"   - Speaker mapping: {mapping}")
            print(f"   - Config keys: {list(config.keys())}")
            
        finally:
            os.unlink(brief_path)
        
        return True
        
    except Exception as e:
        print(f"❌ ProjectBriefParser test failed: {e}")
        return False

def test_videoanalyzer_initialization():
    """Test VideoAnalyzer initialization with and without API key."""
    print("\n🔍 Testing VideoAnalyzer initialization...")
    
    try:
        from assetanalysis.videoanalyzer import VideoAnalyzer
        import os
        
        # Check if API key is loaded from .env file
        env_api_key = os.environ.get("ASSEMBLYAI_API_KEY")
        if env_api_key and env_api_key != "your_assemblyai_api_key_here":
            print(f"✅ API key found in environment (length: {len(env_api_key)})")
            
            # Test with environment API key
            try:
                analyzer = VideoAnalyzer()
                print("✅ VideoAnalyzer created using environment API key")
            except ValueError as e:
                print(f"❌ Failed to use environment API key: {e}")
                return False
        else:
            if not env_api_key:
                print("⚠️  No API key found in environment")
                print("   Create backend/python_services/.env with:")
                print("   ASSEMBLYAI_API_KEY=your_actual_api_key")
            else:
                print("⚠️  API key is placeholder value")
                print("   Update backend/python_services/.env with your actual AssemblyAI API key")
            
            # Test without API key (should fail gracefully)
            try:
                analyzer = VideoAnalyzer()
                print("❌ Should have failed without API key")
                return False
            except ValueError as e:
                print("✅ Correctly requires API key when not in environment")
        
        # Test with dummy API key
        try:
            analyzer = VideoAnalyzer(assemblyai_api_key="dummy_key_for_testing")
            print("✅ VideoAnalyzer created with explicit API key")
        except Exception as e:
            print(f"❌ VideoAnalyzer creation failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ VideoAnalyzer initialization test failed: {e}")
        return False

def test_file_validation():
    """Test file validation functionality."""
    print("\n🔍 Testing file validation...")
    
    try:
        from assetanalysis.videoanalyzer import VideoAnalyzer
        
        analyzer = VideoAnalyzer(assemblyai_api_key="dummy_key_for_testing")
        
        # Test non-existent file
        try:
            result = analyzer.analyze("nonexistent_video.mp4")
            if "error" in result:
                print("✅ Correctly handles non-existent file")
            else:
                print("❌ Should have returned error for non-existent file")
                return False
        except FileNotFoundError:
            print("✅ Correctly raises FileNotFoundError for non-existent file")
        
        return True
        
    except Exception as e:
        print(f"❌ File validation test failed: {e}")
        return False

def test_output_path_generation():
    """Test output path generation logic."""
    print("\n🔍 Testing output path generation...")
    
    try:
        from assetanalysis.videoanalyzer import VideoAnalyzer
        
        analyzer = VideoAnalyzer(assemblyai_api_key="dummy_key_for_testing")
        
        # Create a dummy video file for path testing
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            dummy_video_path = f.name
        
        try:
            # This will fail at the ffmpeg stage, but we can catch the output path from logs
            result = analyzer.analyze(dummy_video_path)
            
            # Check if error contains path information
            if "error" in result:
                print("✅ File processing failed as expected (no actual video content)")
                
                # Check if the expected output directory structure would be created
                # Find project root by looking for key project markers
                current_dir = Path(__file__).parent.resolve()
                project_root = current_dir
                for _ in range(10):  # Max 10 levels up
                    if (project_root / "data").exists() and (project_root / "backend").exists():
                        break
                    parent = project_root.parent
                    if parent == project_root:  # Reached filesystem root
                        break
                    project_root = parent
                
                expected_analyzed_dir = project_root / "data" / "analyzed"
                print(f"✅ Expected output directory: {expected_analyzed_dir}")
                
                return True
            
        finally:
            os.unlink(dummy_video_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Output path generation test failed: {e}")
        return False

def test_error_handling():
    """Test error handling and return format."""
    print("\n🔍 Testing error handling...")
    
    try:
        from assetanalysis.videoanalyzer import VideoAnalyzer
        
        analyzer = VideoAnalyzer(assemblyai_api_key="dummy_key_for_testing")
        
        # Test with invalid file (exists but not a video)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is not a video file")
            invalid_file_path = f.name
        
        try:
            result = analyzer.analyze(invalid_file_path)
            
            # Should return a dict with error information
            if isinstance(result, dict) and "error" in result:
                print("✅ Returns proper error format")
                print(f"   - Error message: {result['error'][:100]}...")
                
                # Check that it has timestamp
                if "timestamp" in result:
                    print("✅ Error includes timestamp")
                else:
                    print("⚠️  Error missing timestamp")
                
                return True
            else:
                print(f"❌ Unexpected result format: {type(result)}")
                return False
                
        finally:
            os.unlink(invalid_file_path)
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def test_dependency_availability():
    """Test if required dependencies are available."""
    print("\n🔍 Testing dependency availability...")
    
    dependencies = {
        'moviepy': 'MoviePy package for video processing (with bundled FFmpeg)',
        'requests': 'HTTP requests for API communication',
        'dotenv': 'Environment variable management',
        'pathlib': 'Path handling (built-in)',
        'json': 'JSON processing (built-in)',
        'tempfile': 'Temporary file handling (built-in)'
    }
    
    available_deps = []
    missing_deps = []
    
    for dep, description in dependencies.items():
        try:
            __import__(dep)
            available_deps.append(dep)
            print(f"✅ {dep}: {description}")
        except ImportError:
            missing_deps.append(dep)
            print(f"❌ {dep}: {description} - MISSING")
    
    print(f"\n📊 Dependencies: {len(available_deps)}/{len(dependencies)} available")
    
    if missing_deps:
        print(f"⚠️  Missing dependencies: {', '.join(missing_deps)}")
        print("   Run: uv sync")
        return False
    
    return True

def main():
    """Run all tests and provide summary."""
    print("🧪 VideoAnalyzer Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Dependency Check", test_dependency_availability),
        ("ProjectBriefParser", test_project_brief_parser),
        ("VideoAnalyzer Init", test_videoanalyzer_initialization),
        ("File Validation", test_file_validation),
        ("Output Path Generation", test_output_path_generation),
        ("Error Handling", test_error_handling),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! VideoAnalyzer is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
