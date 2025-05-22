# Transcript Analysis

A Python tool for generating frame-based video transcripts with speaker detection using AssemblyAI.

## Features

- Ingests video files (MP4, MOV, MKV, etc.)
- Uses AssemblyAI API for high-quality transcription with speaker diarization
- Converts time-based timestamps to frame-based counts
- Outputs a structured JSON with word-level transcript data
- Supports custom spellings for domain-specific terminology

## Requirements

- Python 3.9+
- ffmpeg installed on your system
- AssemblyAI API key

## Installation

```bash
# Install the package
pip install -e .

# Set your AssemblyAI API key as an environment variable
export ASSEMBLYAI_API_KEY="your-api-key-here"

# Or create a .env file in the project root
echo "ASSEMBLYAI_API_KEY=your-api-key-here" > .env
```

## Usage

### Command Line

```bash
# Basic usage
videoanalyzer path/to/your/video.mp4

# Specify output path
videoanalyzer path/to/your/video.mp4 --output path/to/output.json

# Provide API key directly
videoanalyzer path/to/your/video.mp4 --api-key your-api-key-here

# Use custom spellings
videoanalyzer path/to/your/video.mp4 --custom-spell custom_spellings.json
```

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

# Initialize the analyzer
analyzer = VideoAnalyzer(assemblyai_api_key="your-api-key")  # Or use environment variable

# Process a video file
result = analyzer.analyze(
    "path/to/video.mp4", 
    "output.json",
    custom_spell=[
        {
            "from": ["jhon", "jon"],
            "to": "John"
        }
    ]
)

# Access transcript data
print(f"Total words: {len(result['words'])}")
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
  "speakers": ["A", "B"],
  "full_transcript": "Smoke from hundreds of wildfires in Canada is triggering air quality alerts throughout the US...",
  "words": [
    {
      "word": "Smoke",
      "speaker": "A",
      "frame_in": 10,
      "frame_out": 20
    },
    // More words...
  ]
}
```

## How It Works

1. **Audio Extraction**: Extracts audio from the video file
2. **Audio Upload**: Uploads the audio to AssemblyAI servers
3. **Transcription**: Uses AssemblyAI's API to transcribe the audio with speaker labels
4. **Frame Conversion**: Converts millisecond timestamps to frame numbers based on video FPS
5. **Output Generation**: Creates a structured JSON with all transcript data

## Speaker Detection

AssemblyAI's speaker diarization technology automatically identifies different speakers in the audio. The system:

1. Identifies when the speaker changes
2. Assigns consistent labels to each speaker (A, B, C, etc. or Speaker 1, Speaker 2, etc.)
3. Associates every word with its corresponding speaker

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
