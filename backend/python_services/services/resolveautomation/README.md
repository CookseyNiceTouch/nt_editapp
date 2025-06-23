# DaVinci Resolve OTIO Workflow Scripts

This directory contains a comprehensive set of tools for working with OpenTimelineIO (OTIO) files in DaVinci Resolve workflows. The scripts have been refactored to follow single-responsibility principles, with each script focused on one specific task.

## Overview

The workflow consists of **four core scripts** plus a **data pipeline orchestrator**:

### Core Scripts (Single Responsibility)

1. **`exportotio.py`** - Export timelines from DaVinci Resolve to OTIO format
2. **`otio2json.py`** - Convert OTIO files to JSON for editing
3. **`json2otio.py`** - Convert JSON files back to OTIO format
4. **`importotio.py`** - Import OTIO timelines into DaVinci Resolve

### Data Pipeline Orchestrator

5. **`datapipeline.py`** - Orchestrates all operations, manages directories, and chains tasks together

## Directory Structure

```
data/timelineprocessing/
├── timeline_ref/        # Reference timelines (exported from Resolve)
└── timeline_edited/     # Edited timelines (ready for import back to Resolve)
```

## Quick Start

### Basic Workflow

1. **Export a Timeline**:
   ```bash
   uv run datapipeline.py full-export --timeline "My Timeline"
   ```

2. **Edit the JSON** (in `data/timelineprocessing/timeline_ref/`)

3. **Import Back to Resolve**:
   ```bash
   # Copy edited JSON to timeline_edited/ directory, then:
   uv run datapipeline.py full-import --name "Edited Timeline"
   ```

### Individual Script Usage

Each script can also be used independently:

```bash
# Export timeline
uv run exportotio.py --output my_timeline.otio

# Convert to JSON
uv run otio2json.py my_timeline.otio

# Convert back to OTIO
uv run json2otio.py edited_timeline.json

# Import to Resolve
uv run importotio.py timeline.otio --name "New Timeline"
```

## Data Pipeline Commands

The `datapipeline.py` script provides several commands:

### Export Workflows
```bash
# Export current timeline
uv run datapipeline.py export

# Export specific timeline
uv run datapipeline.py export --timeline "Timeline 1"

# Full export workflow (export + convert to JSON)
uv run datapipeline.py full-export
```

### Import Workflows
```bash
# Import timeline (finds most recent OTIO in timeline_edited/)
uv run datapipeline.py import

# Full import workflow (convert JSON to OTIO + import)
uv run datapipeline.py full-import --name "My Edited Timeline"

# Import with source clips
uv run datapipeline.py import --import-clips --clips-path /path/to/media
```

### Conversion Commands
```bash
# Convert OTIO to JSON
uv run datapipeline.py otio2json

# Convert JSON to OTIO
uv run datapipeline.py json2otio

# Disable automatic audio track generation
uv run datapipeline.py json2otio --no-auto-audio
```

### Utility Commands
```bash
# List all files in pipeline directories
uv run datapipeline.py list

# Clean all files from pipeline directories
uv run datapipeline.py clean
```

## Features

### Automatic Audio Track Generation
When converting JSON to OTIO, the system automatically generates matching audio tracks for video clips that reference media files with audio (e.g., MP4, MOV, etc.). This can be disabled with the `--no-auto-audio` flag.

### Smart File Management
- Automatically finds the most recent files when not specified
- Creates necessary directories
- Handles file naming conflicts
- Validates file formats

### Robust Error Handling
- Clear error messages and troubleshooting tips
- Fallback import methods (tries with and without source clips)
- File existence and format validation

## Individual Script Details

### exportotio.py
**Purpose**: Export timeline from DaVinci Resolve to OTIO format

**Key Features**:
- Exports current or specified timeline
- Filename sanitization
- OTIO format validation
- Requires DaVinci Resolve 18.5 Beta 3+ for OTIO export

**Usage**:
```bash
uv run exportotio.py [--output FILE] [--timeline NAME]
```

### otio2json.py
**Purpose**: Convert OTIO files to JSON format for editing

**Key Features**:
- Extracts timeline, track, and clip information
- Flattened metadata structure for easier editing
- Preserves all essential timeline information

**Usage**:
```bash
uv run otio2json.py INPUT_FILE [OUTPUT_FILE]
```

### json2otio.py
**Purpose**: Convert JSON files back to OTIO format

**Key Features**:
- Rebuilds OTIO timeline from JSON data
- Automatic audio track generation
- Project data integration
- Metadata reconstruction

**Usage**:
```bash
uv run json2otio.py INPUT_FILE [OUTPUT_FILE] [--no-auto-audio] [--project-root PATH]
```

### importotio.py
**Purpose**: Import OTIO timelines into DaVinci Resolve

**Key Features**:
- Imports OTIO files into Resolve
- Unique timeline naming (adds suffixes if needed)
- Optional source clips import
- Comprehensive timeline information display

**Usage**:
```bash
uv run importotio.py INPUT_FILE [--name NAME] [--import-clips] [--clips-path PATH]
```

## Requirements

- **DaVinci Resolve** (18.5 Beta 3+ for OTIO export)
- **OpenTimelineIO** (`pip install OpenTimelineIO>=0.16.0`)
- **Python 3.8+**
- **UV** (package manager - used in all scripts)

## Configuration

### DaVinci Resolve Setup
1. Enable scripting in DaVinci Resolve preferences
2. Ensure the following environment variables are set:
   - `RESOLVE_SCRIPT_API`
   - `RESOLVE_SCRIPT_LIB`
   - `PYTHONPATH`

### Project Structure
The scripts auto-detect the project root and create necessary directories. You can override this with the `--project-root` parameter.

## Troubleshooting

### Common Issues

**OTIO Export Not Available**:
- Ensure DaVinci Resolve 18.5 Beta 3 or later
- Check that you're using DaVinci Resolve Studio (free version has limited API access)

**Timeline Import Failed**:
- Ensure media files are imported into the media pool
- Check that file paths in OTIO match your project structure
- Try enabling source clips import

**Script Connection Issues**:
- Verify DaVinci Resolve is running
- Check scripting environment variables
- Ensure scripting is enabled in Resolve preferences

### Error Handling
All scripts provide detailed error messages and troubleshooting suggestions. Use the `list` command to see available files and the `clean` command to reset the pipeline state.

## Example Workflows

### Basic Edit Workflow
```bash
# 1. Export current timeline
uv run datapipeline.py full-export

# 2. Edit the JSON file in data/timelineprocessing/timeline_ref/

# 3. Copy edited JSON to data/timelineprocessing/timeline_edited/

# 4. Import back to Resolve
uv run datapipeline.py full-import --name "Edited Version"
```

### Advanced Workflow with Source Clips
```bash
# Export specific timeline
uv run datapipeline.py export --timeline "Master Timeline"

# Convert to JSON
uv run datapipeline.py otio2json

# [Edit JSON file]

# Convert back to OTIO with custom audio handling
uv run datapipeline.py json2otio --no-auto-audio

# Import with source clips
uv run datapipeline.py import --import-clips --clips-path /media/project/footage
```

---

## Architecture

The refactored architecture follows these principles:

- **Single Responsibility**: Each script does one thing well
- **Composability**: Scripts can be used independently or chained together
- **Flexibility**: The pipeline orchestrator handles common workflows while allowing custom usage
- **Maintainability**: Clear separation of concerns and comprehensive error handling

This design makes the workflow more reliable, easier to debug, and simpler to extend with new features.
