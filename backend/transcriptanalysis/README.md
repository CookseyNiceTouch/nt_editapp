# Transcript Analysis

A Python tool for generating frame-accurate video transcripts with word-level timestamps.

## Features

- Ingests video files (MP4, MOV, MKV, etc.)
- Extracts audio and sends to OpenAI Whisper API
- Generates word-level timestamps
- Converts time-based timestamps to frame-based counts
- Outputs a structured JSON with word-level transcript data

## Requirements

- Python 3.9+
- ffmpeg installed on your system
- OpenAI API key with access to Whisper API

## Installation

```bash
# Install the package
pip install -e .

# Set your OpenAI API key as an environment variable
export OPENAI_API_KEY="your-api-key-here"
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

# Add a prompt to improve transcription accuracy
videoanalyzer path/to/your/video.mp4 --prompt "This is a technical discussion about Python programming"
```

### Python API

```python
from transcriptanalysis.videoanalyzer import VideoAnalyzer

# Initialize the analyzer
analyzer = VideoAnalyzer(openai_api_key="your-api-key")  # Or use environment variable

# Process a video file
result = analyzer.analyze(
    "path/to/video.mp4", 
    "output.json",
    prompt="Optional prompt to guide transcription"
)

# Access transcript data
print(f"Total words: {len(result['words'])}")
print(f"Full transcript: {result['full_transcript']}")
```

## Output Format

The tool generates a JSON file with the following structure:

```json
{
  "file_name": "interview.mp4",
  "fps": 25,
  "duration_frames": 7500,
  "speakers": ["speaker1"],
  "full_transcript": "Hello and welcome to our interview...",
  "words": [
    {
      "word": "Hello",
      "speaker": "speaker1",
      "frame_in": 10,
      "frame_out": 20
    },
    // More words...
  ]
}
```

## Important Notes

1. **Speaker Identification**: The current OpenAI Whisper API doesn't natively support speaker diarization. All transcribed words are assigned to "speaker1" by default. For multi-speaker transcripts, additional processing would be needed.

2. **Model Selection**: The tool uses "whisper-1" model as it's the only model that supports word-level timestamps via the `timestamp_granularities` parameter.

3. **Prompting**: You can improve transcription accuracy by providing a context prompt, especially for domain-specific terms or uncommon words.

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
