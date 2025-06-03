# Transcription API Documentation

A FastAPI-based backend for managing video transcription queues with **full video processing**, designed for Electron frontend integration.

## Key Features

- **🎥 Complete Video Processing**: Upload video files and let VideoAnalyzer handle all processing
- **📦 Queue Management**: Add multiple files to a processing queue
- **📊 Real-time Progress Tracking**: Monitor transcription progress with WebSocket logs  
- **🗂️ File Management**: Organize and retrieve completed transcriptions
- **🔄 Smart Cleanup**: Temporary uploaded videos are automatically cleaned up after processing
- **🎯 Enhanced Transcription**: Speaker detection, custom spellings, project brief integration
- **🔇 Silence Detection**: Configurable silence gap detection and marking

## Architecture

The API serves as a **queue manager** that:
1. **Accepts video file uploads** via REST endpoints
2. **Manages transcription queue** with background processing  
3. **Delegates all video processing** to the existing `VideoAnalyzer` class
4. **Provides real-time status updates** via REST and WebSocket
5. **Handles file lifecycle** including temporary file cleanup

> **Important**: The API works with the existing `VideoAnalyzer` without modifications. VideoAnalyzer handles audio extraction, transcription, and all video processing internally.

## Endpoints

### 📁 Upload Video File
**POST** `/upload`

Upload a video file and add to transcription queue. VideoAnalyzer will handle audio extraction and transcription.

**Parameters:**
- `file` (form-data): Video file (mp4, avi, mov, mkv, wmv, flv, webm)
- `brief_path` (optional): Path to project brief file for enhanced accuracy
- `custom_spell` (optional): JSON string of custom spellings
- `silence_threshold_ms` (optional): Minimum silence duration in ms to mark as silence (default: 1000)

**Response:**
```json
{
  "job_id": "uuid-string",
  "message": "Video uploaded (150.2MB), added to queue", 
  "queue_position": 3
}
```

**Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('file', videoFile);
formData.append('brief_path', '/path/to/brief.txt');
formData.append('custom_spell', JSON.stringify([
  {"from": ["Jon", "john"], "to": "John"},
  {"from": ["AI"], "to": "A.I."}
]));
formData.append('silence_threshold_ms', '2000');

const response = await fetch('/upload', {
  method: 'POST',
  body: formData
});
```

### 📊 Queue Status  
**GET** `/queue`

Get current queue status and all jobs.

**Response:**
```json
{
  "queued_jobs": [
    {
      "id": "job-uuid",
      "status": "queued", 
      "file_name": "interview.mp4",
      "progress": 0,
      "created_at": "2024-01-01T10:00:00Z"
    }
  ],
  "active_jobs": [
    {
      "id": "job-uuid-2",
      "status": "processing_video",
      "file_name": "meeting.mp4", 
      "progress": 45,
      "created_at": "2024-01-01T09:30:00Z",
      "updated_at": "2024-01-01T09:35:00Z"
    }
  ],
  "queue_length": 1,
  "is_processing": true
}
```

#### `GET /job/{job_id}`
Get specific job status and progress.

**Response:**
```json
{
  "id": "job-uuid",
  "status": "processing",
  "file_name": "video.mp4", 
  "progress": 65,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:05:00Z"
}
```

#### `DELETE /queue/{job_id}`
Cancel a specific job (removes from queue or marks active job for cancellation).

**Response:**
```json
{
  "message": "Job {job_id} cancelled successfully"
}
```

#### `DELETE /queue`
Clear all queued jobs (does not affect active jobs).

**Response:**
```json
{
  "message": "Queue cleared successfully"  
}
```

### Analyzed Files Management

#### `GET /analyzed`
Get list of all completed transcription files.

**Response:**
```json
[
  {
    "file_name": "video_uuid.transcript.json",
    "original_video": "video.mp4",
    "analyzed_at": "2024-01-01T12:10:00Z",
    "file_size": 15234,
    "speakers": ["Speaker A", "Speaker B"],
    "duration_frames": 7200,
    "fps": 30.0,
    "word_count": 450,
    "silence_count": 12
  }
]
```

#### `GET /analyzed/{file_name}`
Get specific analyzed transcription file content.

**Response:**
```json
{
  "file_name": "video.mp4",
  "speakers": ["Speaker A", "Speaker B"],
  "words": [
    {
      "word": "Hello",
      "speaker": "Speaker A", 
      "frame_in": 30,
      "frame_out": 45,
      "start_ms": 1000,
      "end_ms": 1500
    }
  ],
  "metadata": {
    "job_id": "uuid",
    "original_file": "video.mp4",
    "analyzed_at": "2024-01-01T12:10:00Z",
    "audio_extracted": true,
    "original_size": 104857600
  }
}
```

#### `DELETE /analyzed/{file_name}`
Delete a specific analyzed file.

**Response:**
```json
{
  "message": "Analyzed file {file_name} deleted successfully"
}
```

### Real-time Monitoring

#### `WebSocket /ws/logs`
Real-time log streaming for monitoring transcription progress.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8001/ws/logs');

ws.onmessage = (event) => {
  const logEntry = JSON.parse(event.data);
  console.log(`[${logEntry.level}] ${logEntry.message}`);
};
```

**Log Entry Format:**
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "logger": "transcription.job.uuid",
  "message": "Audio extraction complete",
  "job_id": "uuid"
}
```

## Processing Workflow

### 1. Video Upload & Audio Extraction
- Video file uploaded via multipart form
- FFmpeg extracts optimized audio (16kHz, mono, PCM)
- Audio filters applied for noise reduction
- Original video file deleted immediately
- Audio size typically 90% smaller than video

### 2. Queue Processing  
- Jobs processed sequentially with ThreadPoolExecutor
- Progress updates: initializing → processing_audio → saving_results → completed
- Real-time progress tracking via WebSocket logs

### 3. AssemblyAI Integration
- Extracted audio uploaded to AssemblyAI
- Enhanced transcription with speaker detection
- Custom vocabulary and spelling corrections applied
- Project brief integration for context

### 4. Results & Cleanup
- Frame-accurate transcript generated 
- Audio file cleaned up after processing
- Results saved as JSON in `/analyzed` directory
- Metadata includes file sizes and processing details

## Error Handling

All endpoints return consistent error responses:

```json
{
  "detail": "Error description",
  "status_code": 400
}
```

Common error codes:
- `400`: Invalid file type or parameters
- `404`: Job or file not found  
- `500`: Processing error (FFmpeg, AssemblyAI, etc.)

## Environment Setup

Required dependencies are managed via `uv`:

```bash
cd backend/transcriptanalysis
uv sync
uv run python -m api
```

Required system dependencies:
- **FFmpeg**: For audio extraction
- **Python 3.9+**: Runtime environment
- **AssemblyAI API Key**: Set as environment variable

## Integration Examples

### TypeScript/Node.js Integration
```typescript
interface UploadRequest {
  file: Buffer;
  fileName: string;
  brief_path?: string;
  silence_threshold_ms?: number;
}

async function uploadVideoFile(request: UploadRequest) {
  const formData = new FormData();
  formData.append('file', new Blob([request.file]), request.fileName);
  
  if (request.brief_path) {
    formData.append('brief_path', request.brief_path);
  }
  
  const response = await fetch('/upload', {
    method: 'POST',
    body: formData
  });
  
  return response.json();
}
```

### React Component Example
```jsx
function VideoUploader() {
  const handleFileUpload = async (files) => {
    for (const file of files) {
      const formData = new FormData();
      formData.append('file', file);
      
      try {
        const response = await fetch('/upload', {
          method: 'POST',
          body: formData
        });
        
        const result = await response.json();
        console.log('Upload successful:', result.message);
        
      } catch (error) {
        console.error('Upload failed:', error);
      }
    }
  };
  
  return (
    <input 
      type="file" 
      accept="video/*"
      onChange={(e) => handleFileUpload(Array.from(e.target.files))}
    />
  );
}
```

## Performance Considerations

- **Storage Optimization**: ~90% space savings through video→audio conversion
- **Processing Speed**: Audio extraction adds 10-30 seconds per file
- **Concurrent Processing**: 2 simultaneous transcription jobs supported
- **Memory Usage**: Streaming file processing prevents memory bloat
- **Network Efficiency**: Only audio sent to AssemblyAI API

## Production Deployment

For production environments:

1. **Configure CORS** for your frontend domain
2. **Set rate limiting** on upload endpoint  
3. **Monitor disk space** in temp directory
4. **Configure logging** for production debugging
5. **Set up health checks** via `GET /` endpoint

The API is designed to be lightweight, efficient, and easy to integrate into existing applications while providing powerful transcription capabilities with minimal storage overhead. 