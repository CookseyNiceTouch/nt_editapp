#!/usr/bin/env python3
"""
Simple Video Transcription API

A minimal FastAPI that replicates main.py behavior as a web service.
Takes video file paths and processes them with VideoAnalyzer.analyze().
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from videoanalyzer import VideoAnalyzer

# FastAPI app
app = FastAPI(
    title="Video Transcription API",
    description="Simple API that replicates main.py behavior for video transcription",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class AnalyzeRequest(BaseModel):
    """Request model for video analysis - exactly like main.py inputs"""
    video_path: str
    output_path: Optional[str] = None
    brief_path: Optional[str] = None
    custom_spell: Optional[List[Dict[str, Any]]] = None
    silence_threshold_ms: int = 1000

class AnalyzeResponse(BaseModel):
    """Response model for analysis results"""
    success: bool
    message: str
    output_file: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Video Transcription API - Replicates main.py behavior",
        "status": "running",
        "version": "1.0.0"
    }

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_video(request: AnalyzeRequest):
    """
    Analyze video - exactly like main.py but as API
    
    This replicates the exact behavior of main.py:
    1. Validate video file exists
    2. Initialize VideoAnalyzer with brief_path
    3. Call analyzer.analyze() with all parameters
    4. Return results
    """
    try:
        # Validate video file exists (like main.py does)
        if not os.path.isfile(request.video_path):
            return AnalyzeResponse(
                success=False,
                message=f"Video file not found: {request.video_path}",
                error=f"Video file not found: {request.video_path}"
            )
        
        # Validate brief file if provided (like main.py does)
        if request.brief_path and not os.path.isfile(request.brief_path):
            return AnalyzeResponse(
                success=False,
                message=f"Brief file not found: {request.brief_path}",
                error=f"Brief file not found: {request.brief_path}"
            )
        
        print(f"🚀 Starting video analysis: {os.path.basename(request.video_path)}")
        print(f"📹 Video: {request.video_path}")
        print(f"📋 Brief: {request.brief_path or 'None'}")
        print(f"📝 Custom Spellings: {len(request.custom_spell) if request.custom_spell else 0} entries")
        print(f"🔇 Silence Threshold: {request.silence_threshold_ms}ms")
        
        # Initialize VideoAnalyzer (exactly like main.py)
        analyzer = VideoAnalyzer(brief_path=request.brief_path)
        
        # Process the video (exactly like main.py)
        result = analyzer.analyze(
            video_path=request.video_path,
            output_path=request.output_path,
            custom_spell=request.custom_spell,
            brief_path=request.brief_path,
            silence_threshold_ms=request.silence_threshold_ms
        )
        
        # Check for errors (like main.py does)
        if "error" in result:
            print(f"❌ Processing failed: {result['error']}")
            return AnalyzeResponse(
                success=False,
                message=f"Processing failed: {result['error']}",
                error=result["error"]
            )
        
        # Determine output file path (like main.py)
        output_file = request.output_path or f"{request.video_path}.transcript.json"
        
        # Success! (like main.py)
        print("✅ Video analysis completed successfully!")
        print(f"📹 File: {result['file_name']}")
        print(f"🎬 FPS: {result['fps']}")
        print(f"⏱️  Duration: {result['duration_frames']} frames")
        print(f"🎤 Speakers: {', '.join(result['speakers'])}")
        print(f"📝 Words: {len([w for w in result['words'] if w['word'] != '**SILENCE**'])}")
        
        silence_count = len([w for w in result['words'] if w['word'] == '**SILENCE**'])
        print(f"🔇 Silence Periods: {silence_count}")
        print(f"💾 Saved to: {output_file}")
        
        return AnalyzeResponse(
            success=True,
            message="Video analysis completed successfully!",
            output_file=output_file,
            result=result
        )
        
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(f"❌ {error_msg}")
        return AnalyzeResponse(
            success=False,
            message=error_msg,
            error=str(e)
        )

def main():
    """Main entry point - start the API server"""
    print("=" * 60)
    print("Video Transcription API - Simple main.py Web Interface")
    print("=" * 60)
    print("Endpoints:")
    print("  GET  /          - Health check")
    print("  POST /analyze   - Analyze video (like main.py)")
    print("  Server: http://127.0.0.1:8001")
    print("=" * 60)
    
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 