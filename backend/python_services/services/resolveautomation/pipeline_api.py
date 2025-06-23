#!/usr/bin/env python3
"""
Pipeline API for AI Agents

Simple Python interface for the DaVinci Resolve OTIO workflow.
Designed for programmatic use by AI agents.
"""

from typing import Optional, Dict, Any
from pathlib import Path
from datapipeline import DataPipeline


class PipelineAPI:
    """
    Simple API interface for AI agents to use the DaVinci Resolve OTIO pipeline.
    
    Usage:
        api = PipelineAPI()
        
        # Workflow 1: Export timeline and convert to JSON
        success = api.export_timeline_to_json()
        
        # Workflow 2: Clear edited files
        success = api.clear_edited_directory()
        
        # Workflow 3: Import edited timeline back to Resolve
        success = api.import_timeline_from_json()
    """
    
    def __init__(self, project_root: Optional[str] = None):
        """
        Initialize the pipeline API.
        
        Args:
            project_root: Path to project root (optional, auto-detected if not provided)
        """
        self.pipeline = DataPipeline(project_root)
    
    def export_timeline_to_json(self, timeline_name: Optional[str] = None) -> bool:
        """
        Workflow 1: Export timeline from Resolve and convert to JSON.
        
        Steps:
        1. Clear contents of timeline_ref folder
        2. Export OTIO from Resolve into timeline_ref
        3. Convert OTIO to JSON
        
        Args:
            timeline_name: Specific timeline name to export (optional, uses current timeline)
            
        Returns:
            True if successful, False otherwise
        """
        return self.pipeline.workflow_1_export(timeline_name)
    
    def clear_edited_directory(self) -> bool:
        """
        Workflow 2: Clear timeline_edited folder.
        
        Returns:
            True if successful, False otherwise
        """
        return self.pipeline.workflow_2_clear_edited()
    
    def import_timeline_from_json(self, timeline_name: Optional[str] = None, import_clips: bool = False) -> bool:
        """
        Workflow 3: Convert JSON to OTIO and import to Resolve.
        
        Steps:
        1. Convert JSON in timeline_edited to OTIO
        2. Import OTIO into Resolve
        
        Args:
            timeline_name: Name for imported timeline (optional)
            import_clips: Whether to import source clips (optional, default False)
            
        Returns:
            True if successful, False otherwise
        """
        return self.pipeline.workflow_3_import(timeline_name, import_clips)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of pipeline directories.
        
        Returns:
            Dictionary with status information
        """
        return self.pipeline.get_status()
    
    def get_ref_json_file(self) -> Optional[Path]:
        """
        Get the path to the JSON file in timeline_ref directory.
        
        Returns:
            Path to JSON file if it exists, None otherwise
        """
        json_files = list(self.pipeline.timeline_ref_dir.glob("*.json"))
        if json_files:
            return max(json_files, key=lambda f: f.stat().st_mtime)
        return None
    
    def get_edited_json_file(self) -> Optional[Path]:
        """
        Get the path to the JSON file in timeline_edited directory.
        
        Returns:
            Path to JSON file if it exists, None otherwise
        """
        json_files = list(self.pipeline.timeline_edited_dir.glob("*.json"))
        if json_files:
            return max(json_files, key=lambda f: f.stat().st_mtime)
        return None
    
    def copy_ref_to_edited(self) -> bool:
        """
        Copy the JSON file from timeline_ref to timeline_edited for editing.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            ref_json = self.get_ref_json_file()
            if not ref_json:
                print("ERROR: No JSON file found in timeline_ref directory")
                return False
            
            # Copy to timeline_edited with timestamp suffix to avoid conflicts
            import time
            timestamp = int(time.time())
            edited_name = f"{ref_json.stem}_{timestamp}.json"
            edited_path = self.pipeline.timeline_edited_dir / edited_name
            
            import shutil
            shutil.copy2(ref_json, edited_path)
            
            print(f"✓ Copied {ref_json.name} to {edited_path.name}")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to copy file: {e}")
            return False


# Convenience functions for AI agents
def export_timeline_to_json(timeline_name: Optional[str] = None) -> bool:
    """Export timeline from Resolve and convert to JSON."""
    api = PipelineAPI()
    return api.export_timeline_to_json(timeline_name)


def clear_edited_directory() -> bool:
    """Clear timeline_edited folder."""
    api = PipelineAPI()
    return api.clear_edited_directory()


def import_timeline_from_json(timeline_name: Optional[str] = None, import_clips: bool = False) -> bool:
    """Convert JSON to OTIO and import to Resolve."""
    api = PipelineAPI()
    return api.import_timeline_from_json(timeline_name, import_clips)


def get_pipeline_status() -> Dict[str, Any]:
    """Get current pipeline status."""
    api = PipelineAPI()
    return api.get_status()


def copy_ref_to_edited() -> bool:
    """Copy JSON from timeline_ref to timeline_edited for editing."""
    api = PipelineAPI()
    return api.copy_ref_to_edited()


if __name__ == "__main__":
    # Example usage
    print("=== Pipeline API Example ===")
    
    api = PipelineAPI()
    
    # Get status
    status = api.get_status()
    print(f"Timeline ref files: {status['timeline_ref']['file_count']}")
    print(f"Timeline edited files: {status['timeline_edited']['file_count']}")
    
    # Check for JSON files
    ref_json = api.get_ref_json_file()
    if ref_json:
        print(f"Found ref JSON: {ref_json.name}")
    
    edited_json = api.get_edited_json_file()
    if edited_json:
        print(f"Found edited JSON: {edited_json.name}") 