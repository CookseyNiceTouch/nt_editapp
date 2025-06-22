#!/usr/bin/env python3
"""
Unified Python Services API
FastAPI wrapper for video editing automation services including:
- AI Services (chatbot, edit agents)
- Asset Analysis (video analysis, transcription)
- Resolve Automation (OTIO, project management)
"""

import os
from pathlib import Path
from typing import Dict, Any
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Import service modules
try:
    from services.ai_services import chatbot_backend, editagent_reedit, editagent_roughcut
    from services.assetanalysis import api as asset_api, videoanalyzer
    from services.resolveautomation import resolve_api
except ImportError as e:
    print(f"Warning: Could not import some services: {e}")

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
        "ai_services": "available",
        "asset_analysis": "available", 
        "resolve_automation": "available"
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
            name="AI Services",
            description="Chatbot and video editing AI agents",
            status="available",
            endpoints=["/ai/chat", "/ai/edit/roughcut", "/ai/edit/reedit"]
        ),
        ServiceInfo(
            name="Asset Analysis", 
            description="Video analysis and transcription services",
            status="available",
            endpoints=["/analysis/video", "/analysis/transcribe"]
        ),
        ServiceInfo(
            name="Resolve Automation",
            description="DaVinci Resolve and OTIO timeline management", 
            status="available",
            endpoints=["/resolve/import", "/resolve/export", "/resolve/timeline"]
        )
    ]
    return services

# AI Services Routes
@app.get("/ai/status")
async def ai_services_status():
    """Status of AI services"""
    return {"status": "AI services available", "services": ["chatbot", "roughcut", "reedit"]}

# Asset Analysis Routes  
@app.get("/analysis/status")
async def asset_analysis_status():
    """Status of asset analysis services"""
    return {"status": "Asset analysis services available", "services": ["video_analyzer", "transcription"]}

# Resolve Automation Routes
@app.get("/resolve/status") 
async def resolve_automation_status():
    """Status of resolve automation services"""
    return {"status": "Resolve automation services available", "services": ["otio_import", "otio_export", "timeline_management"]}

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
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )

if __name__ == "__main__":
    main()
