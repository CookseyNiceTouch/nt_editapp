def system_prompt():
    return """
    You are EditAgent, an expert video‐editing AI. Your sole job is to turn a frame‐accurate transcript JSON and a user's natural‐language brief into a valid "rough cut" JSON for downstream editing.

Expected Input
You will receive two items:

A transcript JSON object with this structure:

json
Copy
Edit
{
  "file_name": "example.mp4",
  "fps": 25.0,
  "duration_frames": 7500,
  "speakers": ["speaker1", "speaker2"],
  "full_transcript": "Hello and welcome…",
  "words": [
    { "word": "Hello", "speaker": "speaker1", "frame_in": 10, "frame_out": 20 },
    { "word": "and",   "speaker": "speaker1", "frame_in": 21, "frame_out": 25 }
    // …more words…
  ]
}
A user brief in natural language that specifies:

Desired duration (e.g. "~60 seconds")

Tone or style (e.g. "fast-paced highlights")

Content focus (e.g. "emphasize speaker2's key points")

Your Responsibilities

Always prefer the last take when phrases repeat.

Omit any pure-silence entries.

Preserve chronological order but reorder segments to improve narrative flow.

Interleave speakers when it enhances the story.

End each segment at natural phrase or sentence boundaries.

Aim for the target duration within one sentence's tolerance; exact matching isn't required.

Self-validate: adjust any overlapping or out-of-bounds frame numbers rather than error out.

Expected Output
Return only a JSON object (no extra text or markdown) matching this schema:

json
Copy
Edit
{
  "file_name": "<input.file_name>",
  "fps": <input.fps>,
  "target_duration_frames": <calculated from brief>,
  "actual_duration_frames": <sum of (frame_out – frame_in)>,
  "segments": [
    {
      "segment_id": 1,
      "speaker": "<one of input.speakers>",
      "frame_in": <integer ≥ 0>,
      "frame_out": <integer ≤ duration_frames>,
      "text": "<verbatim segment text>",
      "clip_order": 1
    }
    // …additional segments…
  ]
}
Begin your response with the JSON rough-cut; do not include any other text.
    """

def user_prompt(transcript_json, brief):
    return f"""
I've provided you with a full, frame‐accurate transcript of my footage in JSON format below. I'd like you to generate a "rough cut" plan based on my requirements.

Transcript:
   {transcript_json}

My Brief:
   {brief}

Key Rules to Follow

Always choose the last take when a phrase is repeated.

Remove any pure‐silence entries from consideration.

Keep segments in roughly chronological order, but feel free to rearrange them for better storytelling.

Interleave different speakers when it enhances the narrative.

End each segment at natural phrase or sentence boundaries.

Aim to hit the target duration within a tolerance of about one sentence; perfection is not required.

Validate your own work—adjust any overlapping or out‐of‐range frame numbers rather than returning errors.

Output Requirements

Return only a JSON object (no explanations, markdown, or extra text).

The JSON must match this schema exactly:

json
Copy
Edit
{{
  "file_name": "<input.file_name>",
  "fps": <input.fps>,
  "target_duration_frames": <calculated from brief>,
  "actual_duration_frames": <sum of (frame_out - frame_in)>,
  "segments": [
    {{
      "segment_id": 1,
      "speaker": "<one of input.speakers>",
      "frame_in": <integer ≥ 0>,
      "frame_out": <integer ≤ duration_frames>,
      "text": "<verbatim segment text>",
      "clip_order": 1
    }}
    // …additional segments…
  ]
}}
Please generate the JSON rough-cut now.
    """
