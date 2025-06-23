#!/usr/bin/env python3
"""
Unified Python Services API
FastAPI wrapper for video editing automation services including:
- Asset Analysis (video analysis, transcription)
"""

import os
import sys
import uuid
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Import service modules
try:
    from services.assetanalysis import api as asset_api, videoanalyzer
except ImportError as e:
    print(f"Warning: Could not import asset analysis services: {e}")

# Initialize FastAPI app
app = FastAPI(
    title="Python Video Services API",
    description="Unified API for video editing automation services",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for web client integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global job tracking dictionary
analysis_jobs: Dict[str, Dict[str, Any]] = {}

# Request/Response models for Asset Analysis
class AnalysisJobRequest(BaseModel):
    video_path: str
    output_path: Optional[str] = None
    brief_path: Optional[str] = None
    custom_spell: Optional[List[Dict[str, Any]]] = None
    silence_threshold_ms: int = 1000

class AnalysisJobResponse(BaseModel):
    job_id: str
    status: str
    message: str
    video_path: str
    created_at: str

class AnalysisStatusResponse(BaseModel):
    job_id: str
    status: str  # "queued", "processing", "completed", "failed"
    message: str
    progress: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    output_file: Optional[str] = None

# Health check and status models
class HealthResponse(BaseModel):
    status: str
    version: str
    services: Dict[str, str]

class ServiceInfo(BaseModel):
    name: str
    description: str
    status: str
    endpoints: list

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Python Video Services API",
        "version": "0.1.0",
        "documentation": "/docs",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint showing status of all services"""
    services_status = {
        "asset_analysis": "available"
    }
    
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        services=services_status
    )

# Service discovery endpoint
@app.get("/services", response_model=list[ServiceInfo])
async def list_services():
    """List all available services and their endpoints"""
    services = [
        ServiceInfo(
            name="Asset Analysis", 
            description="Video analysis and transcription services",
            status="available",
            endpoints=["/analysis/start", "/analysis/status/{job_id}", "/analysis/jobs"]
        )
    ]
    return services

# Asset Analysis Routes
@app.get("/analysis/status")
async def asset_analysis_status():
    """Status of asset analysis services"""
    return {"status": "Asset analysis services available", "services": ["video_analyzer", "transcription"]}

@app.post("/analysis/start", response_model=AnalysisJobResponse)
async def start_analysis(request: AnalysisJobRequest, background_tasks: BackgroundTasks):
    """
    Start a new video analysis job
    
    This endpoint accepts a video file path and analysis parameters,
    creates a job ID, and starts processing in the background.
    """
    try:
        # Validate video file exists
        if not os.path.isfile(request.video_path):
            raise HTTPException(
                status_code=400, 
                detail=f"Video file not found: {request.video_path}"
            )
        
        # Validate brief file if provided
        if request.brief_path and not os.path.isfile(request.brief_path):
            raise HTTPException(
                status_code=400,
                detail=f"Brief file not found: {request.brief_path}"
            )
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Create job record
        job_data = {
            "job_id": job_id,
            "status": "queued",
            "message": "Analysis job created and queued for processing",
            "video_path": request.video_path,
            "output_path": request.output_path,
            "brief_path": request.brief_path,
            "custom_spell": request.custom_spell,
            "silence_threshold_ms": request.silence_threshold_ms,
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "result": None,
            "error": None,
            "output_file": None,
            "progress": "Job queued for processing"
        }
        
        # Store job in global tracking
        analysis_jobs[job_id] = job_data
        
        # Start background processing
        background_tasks.add_task(process_analysis_job, job_id)
        
        return AnalysisJobResponse(
            job_id=job_id,
            status="queued",
            message="Analysis job created and queued for processing",
            video_path=request.video_path,
            created_at=job_data["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create analysis job: {str(e)}")

@app.get("/analysis/status/{job_id}", response_model=AnalysisStatusResponse)
async def get_analysis_status(job_id: str):
    """
    Get the status of a specific analysis job
    
    Returns current status, progress information, and results if completed.
    """
    if job_id not in analysis_jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    job_data = analysis_jobs[job_id]
    
    return AnalysisStatusResponse(
        job_id=job_data["job_id"],
        status=job_data["status"],
        message=job_data["message"],
        progress=job_data.get("progress"),
        created_at=job_data["created_at"],
        completed_at=job_data.get("completed_at"),
        result=job_data.get("result"),
        error=job_data.get("error"),
        output_file=job_data.get("output_file")
    )

@app.get("/analysis/jobs")
async def list_analysis_jobs():
    """
    List all analysis jobs with their current status
    
    Returns a summary of all jobs in the system.
    """
    jobs_summary = []
    for job_id, job_data in analysis_jobs.items():
        jobs_summary.append({
            "job_id": job_id,
            "status": job_data["status"],
            "video_path": job_data["video_path"],
            "created_at": job_data["created_at"],
            "completed_at": job_data.get("completed_at")
        })
    
    return {
        "total_jobs": len(analysis_jobs),
        "jobs": jobs_summary
    }

@app.delete("/analysis/jobs/{job_id}")
async def delete_analysis_job(job_id: str):
    """
    Delete a completed or failed analysis job from tracking
    
    Note: This only removes the job from memory tracking, not the output files.
    """
    if job_id not in analysis_jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    job_data = analysis_jobs[job_id]
    
    # Only allow deletion of completed or failed jobs
    if job_data["status"] in ["processing", "queued"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete job in '{job_data['status']}' status"
        )
    
    del analysis_jobs[job_id]
    
    return {"message": f"Job {job_id} deleted successfully"}

async def process_analysis_job(job_id: str):
    """
    Background task to process video analysis job
    
    This function runs the actual video analysis using the VideoAnalyzer.
    """
    try:
        # Update job status
        analysis_jobs[job_id]["status"] = "processing"
        analysis_jobs[job_id]["message"] = "Video analysis in progress"
        analysis_jobs[job_id]["progress"] = "Initializing video analyzer..."
        
        # Get job parameters
        job_data = analysis_jobs[job_id]
        
        # Add services path for imports
        services_path = os.path.join(os.path.dirname(__file__), "services", "assetanalysis")
        if services_path not in sys.path:
            sys.path.insert(0, services_path)
        
        # Import and initialize VideoAnalyzer
        from videoanalyzer import VideoAnalyzer
        
        analysis_jobs[job_id]["progress"] = "Loading video analyzer..."
        analyzer = VideoAnalyzer(brief_path=job_data["brief_path"])
        
        analysis_jobs[job_id]["progress"] = "Starting video analysis..."
        
        # Process the video
        result = analyzer.analyze(
            video_path=job_data["video_path"],
            output_path=job_data["output_path"],
            custom_spell=job_data["custom_spell"],
            brief_path=job_data["brief_path"],
            silence_threshold_ms=job_data["silence_threshold_ms"]
        )
        
        # Check for errors in result
        if "error" in result:
            analysis_jobs[job_id]["status"] = "failed"
            analysis_jobs[job_id]["message"] = f"Analysis failed: {result['error']}"
            analysis_jobs[job_id]["error"] = result["error"]
            analysis_jobs[job_id]["completed_at"] = datetime.now().isoformat()
            return
        
        # Determine output file path
        output_file = job_data["output_path"] or f"{job_data['video_path']}.transcript.json"
        
        # Success - update job with results
        analysis_jobs[job_id]["status"] = "completed"
        analysis_jobs[job_id]["message"] = "Video analysis completed successfully"
        analysis_jobs[job_id]["completed_at"] = datetime.now().isoformat()
        analysis_jobs[job_id]["result"] = result
        analysis_jobs[job_id]["output_file"] = output_file
        analysis_jobs[job_id]["progress"] = "Analysis completed successfully"
        
    except Exception as e:
        # Handle any processing errors
        analysis_jobs[job_id]["status"] = "failed"
        analysis_jobs[job_id]["message"] = f"Analysis failed with error: {str(e)}"
        analysis_jobs[job_id]["error"] = str(e)
        analysis_jobs[job_id]["completed_at"] = datetime.now().isoformat()
        analysis_jobs[job_id]["progress"] = "Analysis failed"

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Endpoint {request.url.path} not found. Check /docs for available endpoints."}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error. Check logs for details."}
    )

def main():
    """Main entry point for the unified services API"""
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting Python Video Services API on {host}:{port}")
    print("Available endpoints:")
    print("  - API Documentation: http://localhost:8000/docs")
    print("  - Health Check: http://localhost:8000/health") 
    print("  - Services List: http://localhost:8000/services")
    print("  - Asset Analysis:")
    print("    - Start Analysis: POST /analysis/start")
    print("    - Check Status: GET /analysis/status/{job_id}")
    print("    - List Jobs: GET /analysis/jobs")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )

if __name__ == "__main__":
    main()
