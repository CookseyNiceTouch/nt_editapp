# AI Agent Interface for DaVinci Resolve OTIO Workflow

This document explains how AI agents can interact with the DaVinci Resolve OTIO workflow system.

## Three Core Workflows

### Workflow 1: Export Timeline to JSON
**Purpose**: Export the current timeline from DaVinci Resolve and convert to editable JSON format

**Steps**:
1. Clear contents of `timeline_ref` folder
2. Export OTIO from DaVinci Resolve
3. Convert OTIO to JSON

**Usage**:
```python
from pipeline_api import PipelineAPI

api = PipelineAPI()
success = api.export_timeline_to_json()  # Uses current timeline
# OR
success = api.export_timeline_to_json("My Timeline")  # Specific timeline
```

### Workflow 2: Clear Edited Directory
**Purpose**: Clear the `timeline_edited` folder to prepare for new edits

**Usage**:
```python
from pipeline_api import PipelineAPI

api = PipelineAPI()
success = api.clear_edited_directory()
```

### Workflow 3: Import Timeline from JSON
**Purpose**: Convert edited JSON back to OTIO and import into DaVinci Resolve

**Steps**:
1. Convert JSON in `timeline_edited` to OTIO
2. Import OTIO into DaVinci Resolve

**Usage**:
```python
from pipeline_api import PipelineAPI

api = PipelineAPI()
success = api.import_timeline_from_json()  # Auto-generated timeline name
# OR
success = api.import_timeline_from_json("Edited Timeline")  # Custom name
```

## Quick Start for AI Agents

### Method 1: Using the PipelineAPI Class
```python
from pipeline_api import PipelineAPI

# Initialize
api = PipelineAPI()

# Full workflow example
if api.export_timeline_to_json("My Timeline"):
    print("✓ Exported timeline to JSON")
    
    # [AI agent edits the JSON file here]
    
    if api.import_timeline_from_json("AI Edited Timeline"):
        print("✓ Imported edited timeline")
```

### Method 2: Using Convenience Functions
```python
from pipeline_api import (
    export_timeline_to_json,
    clear_edited_directory, 
    import_timeline_from_json,
    get_pipeline_status,
    copy_ref_to_edited
)

# Export timeline
if export_timeline_to_json():
    print("✓ Exported successfully")

# Clear edited directory
clear_edited_directory()

# Import timeline
if import_timeline_from_json("AI Timeline"):
    print("✓ Imported successfully")
```

### Method 3: Using Command Line
```bash
# Export timeline
uv run datapipeline.py workflow-1

# Clear edited directory  
uv run datapipeline.py workflow-2

# Import timeline
uv run datapipeline.py workflow-3 --name "AI Edited Timeline"

# Check status
uv run datapipeline.py status
```

## Directory Structure

```
data/timelineprocessing/
├── timeline_ref/        # Reference timelines (exported from Resolve)
│   ├── exported_timeline.otio
│   └── exported_timeline.json
└── timeline_edited/     # Edited timelines (ready for import back to Resolve)
    ├── edited_timeline.json
    └── edited_timeline.otio
```

## Helper Functions

### Get Pipeline Status
```python
from pipeline_api import get_pipeline_status

status = get_pipeline_status()
print(f"Ref files: {status['timeline_ref']['file_count']}")
print(f"Edited files: {status['timeline_edited']['file_count']}")
```

### Copy Reference to Edited
```python
from pipeline_api import copy_ref_to_edited

# Copy JSON from timeline_ref to timeline_edited for editing
if copy_ref_to_edited():
    print("✓ JSON copied for editing")
```

### Get File Paths
```python
from pipeline_api import PipelineAPI

api = PipelineAPI()

# Get current JSON files
ref_json = api.get_ref_json_file()      # Path to JSON in timeline_ref
edited_json = api.get_edited_json_file()  # Path to JSON in timeline_edited

if ref_json:
    print(f"Reference JSON: {ref_json}")
if edited_json:
    print(f"Edited JSON: {edited_json}")
```

## Error Handling

All functions return `True` for success, `False` for failure. Check return values:

```python
if not api.export_timeline_to_json():
    print("ERROR: Export failed")
    # Handle error
```

## Requirements

- **DaVinci Resolve** (18.5 Beta 3+ for OTIO export)
- **OpenTimelineIO** installed in Python environment
- **UV** package manager (used by scripts)
- **DaVinci Resolve scripting enabled** and environment variables configured

## Common Use Cases for AI Agents

### 1. Basic Edit Workflow
```python
from pipeline_api import PipelineAPI

api = PipelineAPI()

# 1. Export current timeline
if api.export_timeline_to_json():
    # 2. Get the JSON file path
    json_file = api.get_ref_json_file()
    
    # 3. Load and edit JSON
    import json
    with open(json_file, 'r') as f:
        timeline_data = json.load(f)
    
    # [AI edits the timeline_data here]
    
    # 4. Save edited JSON to timeline_edited
    api.clear_edited_directory()
    edited_path = api.pipeline.timeline_edited_dir / "ai_edited.json"
    with open(edited_path, 'w') as f:
        json.dump(timeline_data, f, indent=2)
    
    # 5. Import back to Resolve
    if api.import_timeline_from_json("AI Edited"):
        print("✓ AI editing workflow completed")
```

### 2. Batch Processing
```python
timelines = ["Timeline 1", "Timeline 2", "Timeline 3"]

for timeline_name in timelines:
    api.export_timeline_to_json(timeline_name)
    # [Process each timeline]
    api.import_timeline_from_json(f"AI_{timeline_name}")
```

### 3. Status Monitoring
```python
# Monitor pipeline state
status = get_pipeline_status()
if status['timeline_ref']['file_count'] > 0:
    print("Ready for editing")
if status['timeline_edited']['file_count'] > 0:
    print("Ready for import")
```

## Notes for AI Agents

- Always check return values for error handling
- Use `workflow-2` to clear the edited directory before new operations
- JSON files contain timeline structure, clips, and metadata
- The system automatically handles audio track generation
- File paths are automatically managed by the pipeline
- All operations are designed to be idempotent (safe to run multiple times) 