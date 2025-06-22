import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
import importlib.util

# Set up logging
logger = logging.getLogger(__name__)

# Get paths relative to this file
TOOLCALLING_DIR = Path(__file__).parent.resolve()
SCRIPT_DIR = TOOLCALLING_DIR.parent  # backend/editgenerator
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # Go up to project root
RESOLVE_AUTOMATION_DIR = PROJECT_ROOT / "backend" / "resolveautomation"

# Tool directory file
TOOL_DIRECTORY_PATH = TOOLCALLING_DIR / "tooldiretory.json"

class ToolCaller:
    """Main tool calling system for the chatbot."""
    
    def __init__(self):
        """Initialize the tool caller."""
        self.tools = {}
        self.categories = {}
        self.tool_functions = {}
        self._load_tool_directory()
        self._register_tool_functions()
        
        logger.info(f"ToolCaller initialized with {len(self.tools)} tools across {len(self.categories)} categories")
    
    def _load_tool_directory(self):
        """Load the tool directory from JSON file."""
        if not TOOL_DIRECTORY_PATH.exists():
            logger.error(f"Tool directory not found at: {TOOL_DIRECTORY_PATH}")
            return
        
        try:
            with open(TOOL_DIRECTORY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Load tools
            for tool in data.get("tools", []):
                tool_name = tool.get("name")
                if tool_name:
                    self.tools[tool_name] = tool
            
            # Load categories
            self.categories = data.get("categories", {})
            
            logger.info(f"Loaded {len(self.tools)} tools from directory")
        
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in tool directory: {e}")
        except Exception as e:
            logger.error(f"Error loading tool directory: {e}")
    
    def _register_tool_functions(self):
        """Register the actual Python functions for each tool."""
        # Register all the tool functions
        self.tool_functions = {
            "test_resolve_connection": self._test_resolve_connection,
            "get_resolve_project_info": self._get_resolve_project_info,
            "get_resolve_timeline_info": self._get_resolve_timeline_info,
            "list_resolve_timelines": self._list_resolve_timelines,
            "get_resolve_media_pool_info": self._get_resolve_media_pool_info,
            "export_current_timeline": self._export_current_timeline,
            "check_resolve_environment": self._check_resolve_environment,
            "apply_zoom_to_clip": self._apply_zoom_to_clip,
            "list_clips_in_tracks": self._list_clips_in_tracks,
            "reedit_timeline": self._reedit_timeline,
            "test_reedit_environment": self._test_reedit_environment,
            "generate_roughcut": self._generate_roughcut,
        }
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get a list of all available tools."""
        return list(self.tools.values())
    
    def get_tools_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get tools filtered by category."""
        return [tool for tool in self.tools.values() if tool.get("category") == category]
    
    def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get the schema for a specific tool (for Claude function calling)."""
        tool = self.tools.get(tool_name)
        if not tool:
            return None
        
        return {
            "name": tool["name"],
            "description": tool["description"],
            "input_schema": tool["parameters"]
        }
    
    def get_all_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get schemas for all tools (for Claude function calling)."""
        return [self.get_tool_schema(name) for name in self.tools.keys()]
    
    def call_tool(self, tool_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call a specific tool with given parameters."""
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(self.tools.keys())
            }
        
        if tool_name not in self.tool_functions:
            return {
                "success": False,
                "error": f"Tool function for '{tool_name}' not implemented"
            }
        
        try:
            parameters = parameters or {}
            logger.info(f"Calling tool: {tool_name} with parameters: {parameters}")
            
            # Call the tool function
            result = self.tool_functions[tool_name](**parameters)
            
            return {
                "success": True,
                "tool_name": tool_name,
                "result": result
            }
        
        except Exception as e:
            logger.error(f"Error calling tool '{tool_name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "tool_name": tool_name
            }
    
    # ===== DAVINCI RESOLVE TOOL FUNCTIONS =====
    
    def _get_resolve_api(self):
        """Helper function to get DaVinci Resolve API connection - following exportotio.py pattern."""
        try:
            # Import DaVinci Resolve API
            import DaVinciResolveScript as dvr_script
            
            # Connect to DaVinci Resolve
            resolve = dvr_script.scriptapp("Resolve")
            
            if not resolve:
                return None, "Could not connect to DaVinci Resolve. Make sure DaVinci Resolve is running and scripting is enabled."
            
            return resolve, None
        
        except ImportError as e:
            return None, f"Could not import DaVinciResolveScript module: {e}. Make sure the DaVinci Resolve scripting environment is properly configured."
        except Exception as e:
            return None, f"Error connecting to DaVinci Resolve: {e}"
    
    def _test_resolve_connection(self) -> Dict[str, Any]:
        """Test if DaVinci Resolve is running and accessible."""
        resolve, error = self._get_resolve_api()
        
        if error:
            return {
                "connected": False,
                "error": error,
                "suggestion": "Make sure DaVinci Resolve is running and scripting is enabled"
            }
        
        try:
            # Try to get basic version info - following exportotio.py pattern
            version = resolve.GetVersion()
            
            return {
                "connected": True,
                "version": version,
                "message": "Successfully connected to DaVinci Resolve"
            }
        
        except Exception as e:
            return {
                "connected": False,
                "error": f"Connected but could not get version info: {e}"
            }
    
    def _check_resolve_environment(self) -> Dict[str, Any]:
        """Check if the DaVinci Resolve scripting environment is properly configured."""
        result = {
            "environment_variables": {},
            "paths_exist": {},
            "python_path": [],
            "recommendations": []
        }
        
        # Check environment variables
        env_vars = ["RESOLVE_SCRIPT_API", "RESOLVE_SCRIPT_LIB", "PYTHONPATH"]
        for var in env_vars:
            value = os.environ.get(var)
            result["environment_variables"][var] = value or "Not set"
        
        # Check if paths exist
        resolve_script_api = os.environ.get("RESOLVE_SCRIPT_API")
        resolve_script_lib = os.environ.get("RESOLVE_SCRIPT_LIB")
        
        if resolve_script_api:
            result["paths_exist"]["RESOLVE_SCRIPT_API"] = os.path.exists(resolve_script_api)
        
        if resolve_script_lib:
            result["paths_exist"]["RESOLVE_SCRIPT_LIB"] = os.path.exists(resolve_script_lib)
        
        # Check Python path
        result["python_path"] = sys.path
        
        # Generate recommendations
        if not resolve_script_api:
            result["recommendations"].append("Set RESOLVE_SCRIPT_API environment variable")
        
        if not resolve_script_lib:
            result["recommendations"].append("Set RESOLVE_SCRIPT_LIB environment variable")
        
        if resolve_script_api and not result["paths_exist"].get("RESOLVE_SCRIPT_API"):
            result["recommendations"].append("RESOLVE_SCRIPT_API path does not exist")
        
        if resolve_script_lib and not result["paths_exist"].get("RESOLVE_SCRIPT_LIB"):
            result["recommendations"].append("RESOLVE_SCRIPT_LIB path does not exist")
        
        return result
    
    def _get_resolve_project_info(self) -> Dict[str, Any]:
        """Get information about the currently open project in DaVinci Resolve - following exportotio.py pattern."""
        resolve, error = self._get_resolve_api()
        
        if error:
            return {"error": error}
        
        try:
            # Following the exact pattern from exportotio.py
            project_manager = resolve.GetProjectManager()
            current_project = project_manager.GetCurrentProject()
            
            if not current_project:
                return {"error": "No project is currently open in DaVinci Resolve"}
            
            # Get project info - following exportotio.py pattern
            project_info = {
                "name": current_project.GetName(),
                "timeline_count": current_project.GetTimelineCount(),
                # Get settings that are definitely available
                "current_timeline_name": None
            }
            
            # Try to get current timeline name
            current_timeline = current_project.GetCurrentTimeline()
            if current_timeline:
                project_info["current_timeline_name"] = current_timeline.GetName()
            
            return project_info
        
        except Exception as e:
            return {"error": f"Error getting project info: {e}"}
    
    def _get_resolve_timeline_info(self) -> Dict[str, Any]:
        """Get information about the current timeline in DaVinci Resolve - following exportotio.py pattern."""
        resolve, error = self._get_resolve_api()
        
        if error:
            return {"error": error}
        
        try:
            # Following the exact pattern from exportotio.py
            project_manager = resolve.GetProjectManager()
            current_project = project_manager.GetCurrentProject()
            
            if not current_project:
                return {"error": "No project is currently open"}
            
            current_timeline = current_project.GetCurrentTimeline()
            
            if not current_timeline:
                return {"error": "No timeline is currently active"}
            
            # Following exportotio.py's get_timeline_info function
            timeline_info = {
                "name": current_timeline.GetName(),
                "start_frame": current_timeline.GetStartFrame(),
                "end_frame": current_timeline.GetEndFrame(),
                "start_timecode": current_timeline.GetStartTimecode(),
                "video_tracks": current_timeline.GetTrackCount("video"),
                "audio_tracks": current_timeline.GetTrackCount("audio"),
                "subtitle_tracks": current_timeline.GetTrackCount("subtitle")
            }
            
            # Calculate duration
            timeline_info["duration_frames"] = timeline_info["end_frame"] - timeline_info["start_frame"] + 1
            
            return timeline_info
        
        except Exception as e:
            return {"error": f"Error getting timeline info: {e}"}
    
    def _list_resolve_timelines(self) -> Dict[str, Any]:
        """List all timelines in the current DaVinci Resolve project - following exportotio.py pattern."""
        resolve, error = self._get_resolve_api()
        
        if error:
            return {"error": error}
        
        try:
            # Following the exact pattern from exportotio.py
            project_manager = resolve.GetProjectManager()
            current_project = project_manager.GetCurrentProject()
            
            if not current_project:
                return {"error": "No project is currently open"}
            
            timeline_count = current_project.GetTimelineCount()
            timelines = []
            current_timeline = current_project.GetCurrentTimeline()
            current_timeline_name = current_timeline.GetName() if current_timeline else None
            
            # DaVinci uses 1-based indexing
            for i in range(1, timeline_count + 1):
                timeline = current_project.GetTimelineByIndex(i)
                if timeline:
                    timeline_name = timeline.GetName()
                    timelines.append({
                        "index": i,
                        "name": timeline_name,
                        "is_current": timeline_name == current_timeline_name
                    })
            
            return {
                "timeline_count": timeline_count,
                "current_timeline": current_timeline_name,
                "timelines": timelines
            }
        
        except Exception as e:
            return {"error": f"Error listing timelines: {e}"}
    
    def _get_resolve_media_pool_info(self, include_clips: bool = False) -> Dict[str, Any]:
        """Get information about the media pool in the current DaVinci Resolve project."""
        resolve, error = self._get_resolve_api()
        
        if error:
            return {"error": error}
        
        try:
            # Following the exact pattern from exportotio.py
            project_manager = resolve.GetProjectManager()
            current_project = project_manager.GetCurrentProject()
            
            if not current_project:
                return {"error": "No project is currently open"}
            
            media_pool = current_project.GetMediaPool()
            root_folder = media_pool.GetRootFolder()
            
            def get_folder_info(folder, path=""):
                folder_info = {
                    "name": folder.GetName(),
                    "path": path,
                    "clip_count": 0,
                    "subfolders": []
                }
                
                # Get clips in this folder
                clips = folder.GetClipList()
                if clips:
                    folder_info["clip_count"] = len(clips)
                    
                    if include_clips:
                        folder_info["clips"] = []
                        for clip in clips:
                            try:
                                clip_info = {
                                    "name": clip.GetName(),
                                }
                                # Try to get additional properties safely
                                try:
                                    clip_info["duration"] = clip.GetClipProperty("Duration")
                                    clip_info["fps"] = clip.GetClipProperty("FPS")
                                    clip_info["format"] = clip.GetClipProperty("Type")
                                except:
                                    pass  # Some properties may not be available
                                
                                folder_info["clips"].append(clip_info)
                            except Exception as e:
                                logger.warning(f"Could not get info for clip: {e}")
                
                # Get subfolders
                try:
                    subfolders = folder.GetSubFolderList()
                    if subfolders:
                        for subfolder in subfolders:
                            subfolder_path = f"{path}/{subfolder.GetName()}" if path else subfolder.GetName()
                            folder_info["subfolders"].append(get_folder_info(subfolder, subfolder_path))
                except Exception as e:
                    logger.warning(f"Could not get subfolders: {e}")
                
                return folder_info
            
            media_pool_info = get_folder_info(root_folder)
            
            return media_pool_info
        
        except Exception as e:
            return {"error": f"Error getting media pool info: {e}"}
    
    def _export_current_timeline(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Export the current timeline from DaVinci Resolve to OTIO format - using exportotio.py."""
        try:
            # Import and run the working export function from resolveautomation
            from exportotio import main as export_main
            
            success = export_main()
            
            if success:
                return {
                    "success": True,
                    "message": "Timeline exported successfully using exportotio.py",
                    "output_directory": str(PROJECT_ROOT / "data" / "timelineprocessing" / "timeline_ref")
                }
            else:
                return {
                    "success": False,
                    "error": "Export failed - check DaVinci Resolve connection and active timeline"
                }
        
        except ImportError as e:
            return {"error": f"Could not import export function: {e}"}
        except Exception as e:
            return {"error": f"Error during export: {e}"}
    
    def _apply_zoom_to_clip(
        self, 
        track_index: int, 
        clip_index: int,
        zoom_value: float,
        lock_axes: bool = True,
        description: str = ""
    ) -> Dict[str, Any]:
        """Apply zoom settings to a specific clip for punch-ins and framing adjustments."""
        resolve, error = self._get_resolve_api()
        
        if error:
            return {"error": error}
        
        try:
            # Following the exact pattern from exportotio.py
            project_manager = resolve.GetProjectManager()
            current_project = project_manager.GetCurrentProject()
            
            if not current_project:
                return {"error": "No project is currently open"}
            
            current_timeline = current_project.GetCurrentTimeline()
            
            if not current_timeline:
                return {"error": "No timeline is currently active"}
            
            # Get the specific track
            track_count = current_timeline.GetTrackCount("video")
            if track_index > track_count or track_index < 1:
                return {"error": f"Invalid track index {track_index}. Video tracks available: 1-{track_count}"}
            
            # Get clips from the track
            track_clips = current_timeline.GetItemListInTrack("video", track_index)
            
            if not track_clips or clip_index > len(track_clips) or clip_index < 1:
                return {"error": f"Invalid clip index {clip_index}. Clips available on track {track_index}: 1-{len(track_clips) if track_clips else 0}"}
            
            # Get the specific clip (convert to 0-based indexing)
            target_clip = track_clips[clip_index - 1]
            
            if not target_clip:
                return {"error": f"Could not access clip {clip_index} on track {track_index}"}
            
            # Get clip name for logging
            clip_name = target_clip.GetName()
            
            # Apply zoom using DaVinci Resolve's multiplier system
            # 1.0 = normal size, 1.1 = 10% zoom in, 1.2 = 20% zoom in, etc.
            zoom_properties = {}
            
            # Lock axes together if requested (recommended for uniform punch-ins)
            if lock_axes:
                zoom_properties["ZoomGang"] = True
            
            # Set zoom multipliers
            zoom_properties["ZoomX"] = zoom_value
            zoom_properties["ZoomY"] = zoom_value
            
            # Apply zoom settings
            success = target_clip.SetProperty(zoom_properties)
            
            if success:
                # Prepare result summary
                result = {
                    "success": True,
                    "clip_name": clip_name,
                    "track_index": track_index,
                    "clip_index": clip_index,
                    "zoom_applied": {
                        "zoom_value": zoom_value,
                        "lock_axes": lock_axes,
                        "properties_set": zoom_properties
                    },
                    "description": description,
                    "message": f"Zoom {zoom_value}x applied to '{clip_name}' on track {track_index}"
                }
                
                # Add descriptive summary
                if zoom_value > 1.0:
                    zoom_change = int((zoom_value - 1.0) * 100)
                    result["zoom_summary"] = f"{zoom_change}% zoom in"
                elif zoom_value < 1.0:
                    zoom_change = int((1.0 - zoom_value) * 100)
                    result["zoom_summary"] = f"{zoom_change}% zoom out"
                else:
                    result["zoom_summary"] = "no zoom change (1.0x)"
                
                if lock_axes:
                    result["zoom_summary"] += " (axes locked)"
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"Failed to apply zoom to clip '{clip_name}' on track {track_index}",
                    "clip_name": clip_name,
                    "track_index": track_index,
                    "clip_index": clip_index
                }
        
        except Exception as e:
            return {"error": f"Error applying zoom: {e}"}
    
    def _list_clips_in_tracks(self, track_type: str = "video") -> Dict[str, Any]:
        """List all clips across tracks with their positions and details."""
        resolve, error = self._get_resolve_api()
        
        if error:
            return {"error": error}
        
        try:
            # Following the exact pattern from exportotio.py
            project_manager = resolve.GetProjectManager()
            current_project = project_manager.GetCurrentProject()
            
            if not current_project:
                return {"error": "No project is currently open"}
            
            current_timeline = current_project.GetCurrentTimeline()
            
            if not current_timeline:
                return {"error": "No timeline is currently active"}
            
            # Get track count for the specified type
            track_count = current_timeline.GetTrackCount(track_type)
            
            if track_count == 0:
                return {
                    "track_type": track_type,
                    "track_count": 0,
                    "tracks": [],
                    "message": f"No {track_type} tracks found in current timeline"
                }
            
            tracks_info = []
            total_clips = 0
            
            # Iterate through each track (1-based indexing)
            for track_index in range(1, track_count + 1):
                track_clips = current_timeline.GetItemListInTrack(track_type, track_index)
                
                track_info = {
                    "track_index": track_index,
                    "clip_count": len(track_clips) if track_clips else 0,
                    "clips": []
                }
                
                if track_clips:
                    for clip_index, clip in enumerate(track_clips, 1):  # 1-based indexing
                        try:
                            clip_info = {
                                "clip_index": clip_index,
                                "name": clip.GetName(),
                                "start": clip.GetStart(),
                                "end": clip.GetEnd(),
                                "duration": clip.GetDuration()
                            }
                            
                            # Try to get additional properties safely
                            try:
                                clip_info["source_file"] = clip.GetMediaPoolItem().GetClipProperty("File Path") if clip.GetMediaPoolItem() else "Unknown"
                            except:
                                clip_info["source_file"] = "Unknown"
                            
                            # For video clips, try to get resolution info
                            if track_type == "video":
                                try:
                                    media_item = clip.GetMediaPoolItem()
                                    if media_item:
                                        clip_info["resolution"] = f"{media_item.GetClipProperty('Resolution')}"
                                        clip_info["fps"] = media_item.GetClipProperty("FPS")
                                except:
                                    pass
                            
                            track_info["clips"].append(clip_info)
                            total_clips += 1
                        
                        except Exception as e:
                            logger.warning(f"Could not get info for clip {clip_index} on track {track_index}: {e}")
                            track_info["clips"].append({
                                "clip_index": clip_index,
                                "name": "Unknown",
                                "error": str(e)
                            })
                
                tracks_info.append(track_info)
            
            return {
                "track_type": track_type,
                "track_count": track_count,
                "total_clips": total_clips,
                "tracks": tracks_info,
                "timeline_name": current_timeline.GetName()
            }
        
        except Exception as e:
            return {"error": f"Error listing clips: {e}"}
    
    def _reedit_timeline(
        self,
        instructions: str,
        description: str = ""
    ) -> Dict[str, Any]:
        """Apply comprehensive editing instructions to the current timeline using the re-edit agent."""
        try:
            logger.info(f"Starting direct re-edit function call")
            logger.info(f"Instructions: {instructions}")
            
            # Import the main function from editagent_reedit
            try:
                # Add the parent directory to sys.path to import editagent_reedit
                if str(SCRIPT_DIR) not in sys.path:
                    sys.path.insert(0, str(SCRIPT_DIR))
                
                from editagent_reedit import main_reedit_workflow
                
                # Call the function directly with silent=True for tool use
                result = main_reedit_workflow(
                    user_instructions=instructions,
                    silent=True  # Silent mode for tool calling
                )
                
                # Enhance the result with our tool metadata
                if result.get("success"):
                    enhanced_result = {
                        "success": True,
                        "instructions": instructions,
                        "description": description,
                        "message": "Timeline re-editing completed successfully via direct function call",
                        **result  # Include all the original result data
                    }
                    
                    logger.info(f"Re-edit completed successfully: {enhanced_result.get('timeline_name', 'Unknown timeline')}")
                    return enhanced_result
                else:
                    # Function returned an error
                    logger.error(f"Re-edit function failed: {result.get('error', 'Unknown error')}")
                    return {
                        "success": False,
                        "error": result.get('error', 'Unknown error from re-edit function'),
                        "instructions": instructions,
                        "description": description,
                        "function_result": result
                    }
                    
            except ImportError as e:
                logger.error(f"Failed to import editagent_reedit: {e}")
                return {
                    "success": False,
                    "error": f"Failed to import re-edit module: {e}",
                    "instructions": instructions
                }
        
        except Exception as e:
            logger.error(f"Error in direct re-edit call: {e}")
            logger.exception("Full traceback:")
            return {
                "success": False,
                "error": f"Unexpected error in direct function call: {e}",
                "instructions": instructions
            }
    
    def _test_reedit_environment(self) -> Dict[str, Any]:
        """Test the re-edit environment and module import capabilities."""
        try:
            # Check if the script exists
            script_path = SCRIPT_DIR / "editagent_reedit.py"
            
            diagnostic_info = {
                "script_exists": script_path.exists(),
                "script_path": str(script_path),
                "working_directory": str(SCRIPT_DIR),
                "python_version": sys.version,
                "environment_variables": {},
                "import_test": {},
                "function_test": {}
            }
            
            # Check key environment variables
            key_env_vars = ["claude_api_key", "RESOLVE_SCRIPT_API", "RESOLVE_SCRIPT_LIB"]
            for var in key_env_vars:
                value = os.environ.get(var)
                diagnostic_info["environment_variables"][var] = "SET" if value else "NOT_SET"
            
            # Test importing the re-edit module
            try:
                if str(SCRIPT_DIR) not in sys.path:
                    sys.path.insert(0, str(SCRIPT_DIR))
                
                import editagent_reedit
                diagnostic_info["import_test"]["editagent_reedit"] = {
                    "success": True,
                    "module_path": editagent_reedit.__file__ if hasattr(editagent_reedit, '__file__') else "Unknown"
                }
                
                # Test importing the main function
                from editagent_reedit import main_reedit_workflow
                diagnostic_info["import_test"]["main_function"] = {
                    "success": True,
                    "function_type": str(type(main_reedit_workflow))
                }
                
                # Test a dry run call (with invalid data to ensure it fails gracefully)
                try:
                    # This should fail but not crash - testing the function signature
                    test_result = main_reedit_workflow(
                        user_instructions="test instruction",
                        silent=True
                    )
                    
                    # If we get here, the function call worked (even if it returned an error)
                    diagnostic_info["function_test"]["call_test"] = {
                        "success": True,
                        "returns_dict": isinstance(test_result, dict),
                        "has_success_field": "success" in test_result if isinstance(test_result, dict) else False,
                        "result_preview": str(test_result)[:200] if test_result else "No result"
                    }
                    
                except Exception as func_error:
                    diagnostic_info["function_test"]["call_test"] = {
                        "success": False,
                        "error": str(func_error),
                        "error_type": type(func_error).__name__
                    }
                
            except ImportError as import_error:
                diagnostic_info["import_test"]["editagent_reedit"] = {
                    "success": False,
                    "error": str(import_error),
                    "error_type": "ImportError"
                }
            except Exception as general_error:
                diagnostic_info["import_test"]["general_error"] = {
                    "success": False,
                    "error": str(general_error),
                    "error_type": type(general_error).__name__
                }
            
            # Check dependencies that the re-edit module needs
            required_modules = ["anthropic", "jsonschema", "dotenv"]
            diagnostic_info["dependencies"] = {}
            
            for module_name in required_modules:
                try:
                    __import__(module_name)
                    diagnostic_info["dependencies"][module_name] = "AVAILABLE"
                except ImportError:
                    diagnostic_info["dependencies"][module_name] = "MISSING"
            
            return {
                "success": True,
                "diagnostic_info": diagnostic_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error running diagnostics: {e}"
            }
    
    def _generate_roughcut(
        self,
        description: str = ""
    ) -> Dict[str, Any]:
        """Generate a rough cut timeline from transcript data using the roughcut agent."""
        try:
            logger.info(f"Starting direct roughcut generation function call")
            logger.info(f"Description: {description}")
            
            # Import the main function from editagent_roughcut
            try:
                # Add the parent directory to sys.path to import editagent_roughcut
                if str(SCRIPT_DIR) not in sys.path:
                    sys.path.insert(0, str(SCRIPT_DIR))
                
                from editagent_roughcut import main_roughcut_workflow
                
                # Call the function directly with silent=True for tool use
                result = main_roughcut_workflow(
                    silent=True  # Silent mode for tool calling
                )
                
                # Enhance the result with our tool metadata
                if result.get("success"):
                    enhanced_result = {
                        "success": True,
                        "description": description,
                        "message": "Rough cut generation completed successfully via direct function call",
                        **result  # Include all the original result data
                    }
                    
                    logger.info(f"Roughcut completed successfully: {enhanced_result.get('timeline_name', 'Unknown timeline')}")
                    return enhanced_result
                else:
                    # Function returned an error
                    logger.error(f"Roughcut function failed: {result.get('error', 'Unknown error')}")
                    return {
                        "success": False,
                        "error": result.get('error', 'Unknown error from roughcut function'),
                        "description": description,
                        "function_result": result
                    }
                    
            except ImportError as e:
                logger.error(f"Failed to import editagent_roughcut: {e}")
                return {
                    "success": False,
                    "error": f"Failed to import roughcut module: {e}",
                    "description": description
                }
        
        except Exception as e:
            logger.error(f"Error in direct roughcut call: {e}")
            logger.exception("Full traceback:")
            return {
                "success": False,
                "error": f"Unexpected error in direct function call: {e}",
                "description": description
            }

# Global instance for easy access
tool_caller = ToolCaller()

# Convenience functions
def get_available_tools() -> List[Dict[str, Any]]:
    """Get all available tools."""
    return tool_caller.get_available_tools()

def call_tool(tool_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
    """Call a tool by name."""
    return tool_caller.call_tool(tool_name, parameters)

def get_tool_schemas_for_claude() -> List[Dict[str, Any]]:
    """Get tool schemas formatted for Claude function calling."""
    return tool_caller.get_all_tool_schemas()

if __name__ == "__main__":
    # Test the tool system
    print("=== Tool Caller Test ===")
    
    tools = get_available_tools()
    print(f"Available tools: {len(tools)}")
    
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    print("\n=== Testing DaVinci Resolve Connection ===")
    result = call_tool("test_resolve_connection")
    print(f"Connection test result: {result}")
    
    print("\n=== Testing Environment Check ===")
    env_result = call_tool("check_resolve_environment")
    print(f"Environment check: {env_result}")
