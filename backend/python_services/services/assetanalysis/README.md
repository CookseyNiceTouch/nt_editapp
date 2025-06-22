# Transcript Analysis

A Python tool for generating frame-based video transcripts with speaker detection using AssemblyAI.

**New**: Now includes a FastAPI-based backend for Electron frontend integration!

## Features

- Ingests video files (MP4, MOV, MKV, etc.)
- Uses AssemblyAI API for high-quality transcription with speaker diarization
- Converts time-based timestamps to frame-based counts
- Outputs a structured JSON with word-level transcript data
- Supports custom spellings for domain-specific terminology
- **NEW**: RESTful API for queue management and progress tracking
- **NEW**: Automatic silence detection and marking
- **NEW**: Project brief integration for improved accuracy

## Requirements

- Python 3.9+
- ffmpeg installed on your system
- AssemblyAI API key

## Installation

```bash
# Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install -e .

# Set your AssemblyAI API key as an environment variable
export ASSEMBLYAI_API_KEY="your-api-key-here"

# Or create a .env file in the project root
echo "ASSEMBLYAI_API_KEY=your-api-key-here" > .env
```

## Usage

### API Backend (Recommended for Electron Integration)

Start the FastAPI server for frontend integration:

```bash
# Start the API server
python -m transcriptanalysis.api

# Or using the entry point
transcription-api

# API will be available at http://127.0.0.1:8000
# Auto-generated docs at http://127.0.0.1:8000/docs
```

**Key API Features:**
- Queue-based processing with progress tracking
- File upload or path-based job submission
- Real-time job status monitoring
- Automatic processing of queued files
- Completed transcript management in `./data/analyzed/`

See [API_README.md](API_README.md) for complete API documentation.

### Interactive Console Tool

```bash
# Launch interactive console interface
python backend/transcriptanalysis/main.py

# Follow the prompts to configure transcription settings
```

### Command Line (Legacy)

```bash
# Basic usage
videoanalyzer path/to/your/video.mp4

# Enhanced with project brief and silence detection
videoanalyzer path/to/your/video.mp4 --brief project_brief.txt --silence-threshold 1500

# Specify output path
videoanalyzer path/to/your/video.mp4 --output path/to/output.json

# Use custom spellings
videoanalyzer path/to/your/video.mp4 --custom-spell custom_spellings.json
```

### Project Brief Integration

Create a project brief file to improve transcription accuracy:

```text
Title: "AI Innovation Summit 2024"
Talent: John Smith, Sarah Wilson
Objective: Panel discussion on artificial intelligence trends
Core Message: Exploring the future of AI in business applications

The speakers will discuss machine learning, neural networks, 
and "digital transformation" strategies.
```

The system will automatically:
- Extract speaker names for better diarization
- Identify key vocabulary for word boosting
- Apply custom spelling corrections

### Custom Spellings

You can create a JSON file with custom spellings to improve transcription accuracy:

```json
[
  {
    "from": ["jhon", "jon"],
    "to": "John"
  },
  {
    "from": ["artifical intelligence", "A I"],
    "to": "AI"
  }
]
```

### Python API

```python
from transcriptanalysis.videoanalyzer import VideoAnalyzer

# Initialize with project brief for enhanced accuracy
analyzer = VideoAnalyzer(
    assemblyai_api_key="your-api-key",
    brief_path="project_brief.txt"
)

# Process a video file with silence detection
result = analyzer.analyze(
    "path/to/video.mp4", 
    "output.json",
    custom_spell=[
        {
            "from": ["jhon", "jon"],
            "to": "John"
        }
    ],
    silence_threshold_ms=1000  # Mark silences longer than 1 second
)

# Access transcript data
print(f"Total words: {len([w for w in result['words'] if w['word'] != '**SILENCE**'])}")
print(f"Silence periods: {len([w for w in result['words'] if w['word'] == '**SILENCE**'])}")
print(f"Speakers detected: {result['speakers']}")
print(f"Full transcript: {result['full_transcript']}")
```

## Output Format

The tool generates a JSON file with the following structure:

```json
{
  "file_name": "interview.mp4",
  "fps": 25,
  "duration_frames": 7500,
  "speakers": ["John Smith", "Sarah Wilson"],
  "full_transcript": "Smoke from hundreds of wildfires in Canada is triggering air quality alerts throughout the US...",
  "silence_threshold_ms": 1000,
  "words": [
    {
      "word": "Smoke",
      "speaker": "John Smith",
      "frame_in": 10,
      "frame_out": 20,
      "confidence": 0.95
    },
    {
      "word": "**SILENCE**",
      "speaker": "**SILENCE**",
      "frame_in": 150,
      "frame_out": 180,
      "confidence": 1.0,
      "duration_ms": 1200
    }
    // More words...
  ],
  "metadata": {
    "job_id": "uuid-string",
    "original_file": "interview.mp4",
    "analyzed_at": "2024-01-01T12:00:00Z",
    "silence_threshold_ms": 1000
  }
}
```

## Directory Structure

```
backend/transcriptanalysis/
├── api.py                 # FastAPI backend server
├── videoanalyzer.py       # Core transcription engine
├── main.py               # Interactive console interface
├── test_api.py           # API testing client
├── data/
│   ├── analyzed/         # Completed transcriptions
│   ├── queue/           # Queue persistence
│   └── temp/            # Temporary files
└── README.md            # This file
```

## How It Works

1. **Audio Extraction**: Extracts high-quality audio from video file
2. **Brief Analysis**: Parses project brief for context enhancement
3. **Audio Upload**: Uploads audio to AssemblyAI servers
4. **Enhanced Transcription**: Uses AssemblyAI with custom vocabulary and speaker hints
5. **Frame Conversion**: Converts timestamps to frame numbers with silence detection
6. **Output Generation**: Creates structured JSON with metadata

## Enhanced Features

### Speaker Detection & Mapping
- Automatic speaker diarization
- Project brief integration for speaker name mapping
- Confidence scoring for speaker assignments

### Silence Detection
- Configurable silence threshold (default: 1000ms)
- Automatic silence period marking
- Frame-accurate silence boundaries

### Accuracy Improvements
- Project brief vocabulary extraction
- Custom spelling corrections
- Speaker name normalization
- High-quality audio preprocessing

## Error Handling

If processing fails, the tool will:
1. Exit with a non-zero status code
2. Generate a minimal JSON with error details:

```json
{
  "error": "Error message",
  "timestamp": "2023-05-19T15:00:00Z"
}
```

## Development & Testing

```bash
# Test the API endpoints
python backend/transcriptanalysis/test_api.py

# Run interactive console
python backend/transcriptanalysis/main.py

# Start API server with auto-reload
python -m transcriptanalysis.api
```

## Electron Frontend Integration

The FastAPI backend is designed for seamless Electron integration:

1. **Queue Management**: Add multiple files for batch processing
2. **Real-time Progress**: WebSocket or polling for live updates
3. **File Management**: CRUD operations for analyzed transcripts
4. **Error Handling**: Comprehensive error reporting and recovery

See [API_README.md](API_README.md) for detailed integration examples.
