# AI-Editor Module

The AI-Editor module processes video transcripts and user briefs to generate edited segment lists for video rough cuts.

## Features

- Consumes frame-based transcript JSON from the VideoAnalyzer module
- Processes user briefs to understand editing requirements
- Generates a curated, ordered list of segments with frame in/out points
- Uses Claude 3.7 Sonnet with extended thinking for improved reasoning

## Installation

1. Ensure you have Python 3.9+ installed
2. Install the package and its dependencies:

```bash
pip install -e .
```

3. Create a `.env` file in the project root with your Claude API key:

```
claude_api_key=your_api_key_here
```

## Usage

### Basic Usage

```python
from editgenerator.main import process_transcript

# Load your transcript data
transcript_data = {
    "file_name": "example.mp4",
    "fps": 30.0,
    "duration_frames": 3600,
    "speakers": ["speaker1", "speaker2"],
    "full_transcript": "...",
    "words": [
        {"word": "Hello", "speaker": "speaker1", "frame_in": 10, "frame_out": 20},
        # More words...
    ]
}

# Define your editing brief
user_brief = "Create a ~60 seconds highlight focusing on the key points about AI technology."

# Process the transcript
result = process_transcript(transcript_data, user_brief)

# The result will be a JSON object with the edited segments
```

### Example Script

You can run the included example script:

```bash
python example.py [path_to_transcript.json]
```

If no transcript file is provided, the script will use a mock example.

## Input Format

The module expects transcript data in the following format:

```json
{
  "file_name": "example.mp4",
  "fps": 30.0,
  "duration_frames": 3600,
  "speakers": ["speaker1", "speaker2"],
  "full_transcript": "Complete transcript text...",
  "words": [
    {
      "word": "Hello",
      "speaker": "speaker1",
      "frame_in": 10,
      "frame_out": 20
    },
    // Additional words...
  ]
}
```

## Output Format

The module produces edited segment data in the following format:

```json
{
  "file_name": "example.mp4",
  "fps": 30.0,
  "target_duration_frames": 1800,
  "actual_duration_frames": 1792,
  "segments": [
    {
      "segment_id": 1,
      "speaker": "speaker2",
      "frame_in": 150,
      "frame_out": 300,
      "text": "The main point here...",
      "clip_order": 1
    },
    // More segments...
  ]
}
```

## User Brief Guidelines

The user brief should include:

- Target duration (e.g., "~60 seconds")
- Tone/style (e.g., "fast-paced highlights")
- Content priorities (e.g., "focus on speaker2's key points")

Example: "Create a ~90 second highlight reel focusing on the technical explanations with a professional tone."

## Error Handling

If processing fails, the module will return an error object:

```json
{
  "error": "Error message describing what went wrong",
  "details": { /* Additional information */ }
}
```
