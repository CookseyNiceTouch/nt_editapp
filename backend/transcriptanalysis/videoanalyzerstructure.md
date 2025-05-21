# VideoAnalyzer JSON Structure

This document describes the structure and format of JSON files produced by the VideoAnalyzer tool, designed to be easily parsed by AI systems.

## Overview

The JSON output represents a frame-accurate transcription of a video file. All timing information is converted from seconds to frame numbers, making it suitable for video editing and processing tasks.

## Top-Level Structure

```json
{
  "file_name": "example.mp4",
  "fps": 30.0,
  "duration_frames": 3600,
  "speakers": ["speaker1"],
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

## Field Descriptions

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `file_name` | string | The original filename of the processed video |
| `fps` | number (float) | Frames per second of the video |
| `duration_frames` | number (integer) | Total number of frames in the video |
| `speakers` | array of strings | List of unique speaker identifiers found in the transcript |
| `full_transcript` | string | Complete text transcript of the entire video |

### Words Array

The `words` array contains objects representing individual words detected in the audio, with the following properties:

| Field | Type | Description |
|-------|------|-------------|
| `word` | string | The transcribed word |
| `speaker` | string | Speaker identifier (currently always "speaker1") |
| `frame_in` | number (integer) | Starting frame where the word begins |
| `frame_out` | number (integer) | Ending frame where the word ends |

## Frame Calculation

Frame numbers are calculated from timestamps using the formula:
```
frame = round(time_in_seconds * fps)
```

For example, if a word starts at 1.5 seconds in a 30fps video, the `frame_in` value would be `round(1.5 * 30) = 45`.

## Error Format

If processing fails, the JSON will have a different structure:

```json
{
  "error": "Error message describing what went wrong",
  "timestamp": "2023-10-01T15:00:00Z"
}
```

## Parsing Guidelines for AI

1. **Frame Sequence Verification**: Frame numbers should always increase (frame_in₁ < frame_out₁ ≤ frame_in₂). If not, there may be data corruption.

2. **Speaker Consistency**: All entries in the `words` array should have speaker values that match entries in the `speakers` array.

3. **Frame Range Validation**: All frame numbers should be non-negative and less than `duration_frames`.

4. **Transcript Reconstruction**: The full transcript can be reconstructed by joining all words with appropriate spacing, though timing information would be lost.

5. **Word Timing**: To locate a word in the video, use its `frame_in` and `frame_out` values to determine start and end times:
   ```
   time_in_seconds = frame_number / fps
   ```

## JSON Schema

For validation purposes, the following JSON Schema can be used:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["file_name", "fps", "duration_frames", "speakers", "full_transcript", "words"],
  "properties": {
    "file_name": {
      "type": "string",
      "description": "Original filename of the video"
    },
    "fps": {
      "type": "number",
      "description": "Frames per second of the video"
    },
    "duration_frames": {
      "type": "integer",
      "description": "Total number of frames in the video"
    },
    "speakers": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "List of unique speaker identifiers"
    },
    "full_transcript": {
      "type": "string",
      "description": "Complete transcript text"
    },
    "words": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["word", "speaker", "frame_in", "frame_out"],
        "properties": {
          "word": {
            "type": "string"
          },
          "speaker": {
            "type": "string"
          },
          "frame_in": {
            "type": "integer",
            "minimum": 0
          },
          "frame_out": {
            "type": "integer",
            "minimum": 0
          }
        }
      }
    }
  },
  "additionalProperties": false
}
```

## Example Use Cases

1. **Finding words at a specific frame**: 
   ```python
   def find_words_at_frame(data, target_frame):
       return [word for word in data["words"] 
              if word["frame_in"] <= target_frame <= word["frame_out"]]
   ```

2. **Getting a time-window transcript**:
   ```python
   def get_transcript_between_frames(data, start_frame, end_frame):
       words_in_range = [word["word"] for word in data["words"]
                        if (word["frame_in"] >= start_frame and 
                            word["frame_out"] <= end_frame)]
       return " ".join(words_in_range)
   ```

3. **Calculating word duration in seconds**:
   ```python
   def get_word_duration(word, fps):
       frames = word["frame_out"] - word["frame_in"]
       return frames / fps
   ```
