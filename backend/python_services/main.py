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
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

# Import service modules
try:
    from services.assetanalysis import videoanalyzer
except ImportError as e:
    print(f"Warning: Could not import asset analysis services: {e}")

try:
    from services.ai_services.chatbot_backend import ChatbotBackend, list_conversations
except ImportError as e:
    print(f"Warning: Could not import chatbot services: {e}")
    ChatbotBackend = None

# Initialize FastAPI app
app = FastAPI(
    title="Python Video Services API",
    description="Unified API for video editing automation services including AI chatbot",
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

# Global chatbot instances tracking
chatbot_instances: Dict[str, Any] = {}  # Use Any instead of ChatbotBackend to avoid linter error

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

# Request/Response models for Chatbot
class ChatbotCreateRequest(BaseModel):
    conversation_id: Optional[str] = None
    enable_tools: bool = True

class ChatbotCreateResponse(BaseModel):
    conversation_id: str
    welcome_message: str
    tools_enabled: bool
    created_at: str

class ChatbotToggleToolsRequest(BaseModel):
    enable_tools: bool

class ChatbotToggleToolsResponse(BaseModel):
    conversation_id: str
    tools_enabled: bool
    message: str

class ChatbotProjectInfoResponse(BaseModel):
    project_loaded: bool
    project_title: Optional[str] = None
    brief_length: Optional[int] = None
    brief_preview: Optional[str] = None

class ChatbotWelcomeResponse(BaseModel):
    welcome_message: str
    conversation_id: str

class ChatbotMessageRequest(BaseModel):
    message: str
    conversation_id: str
    stream: bool = True

class ChatbotMessageResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    thinking: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    conversation_id: str
    message_count: int
    error: Optional[str] = None

class ChatbotConversationInfo(BaseModel):
    conversation_id: str
    message_count: int
    created_at: Optional[str] = None
    last_message_at: Optional[str] = None
    tools_enabled: bool

class ChatbotToolRequest(BaseModel):
    tool_name: str
    parameters: Optional[Dict[str, Any]] = None
    conversation_id: str

class ChatbotToolResponse(BaseModel):
    success: bool
    tool_name: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

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
    
    # Add chatbot services if available
    if ChatbotBackend is not None:
        services.append(ServiceInfo(
            name="AI Chatbot",
            description="Conversational AI with tool calling capabilities",
            status="available",
            endpoints=[
                "/chatbot/conversations",
                "/chatbot/conversations/{conversation_id}/message",
                "/chatbot/conversations/{conversation_id}/message/stream",
                "/chatbot/tools"
            ]
        ))
    else:
        services.append(ServiceInfo(
            name="AI Chatbot",
            description="Conversational AI with tool calling capabilities",
            status="unavailable",
            endpoints=[]
        ))
    
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
        # Normalize the video path for Windows compatibility
        normalized_video_path = os.path.normpath(request.video_path)
        
        # Validate video file exists
        if not os.path.isfile(normalized_video_path):
            raise HTTPException(
                status_code=400, 
                detail=f"Video file not found: {normalized_video_path}"
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
            "video_path": normalized_video_path,
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
            video_path=normalized_video_path,
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

# Chatbot Routes
@app.get("/chatbot/status")
async def chatbot_status():
    """Enhanced status of chatbot services with detailed information"""
    if ChatbotBackend is None:
        return {"status": "Chatbot services not available", "error": "ChatbotBackend not imported"}
    
    # Get project info
    project_info = {"loaded": False}
    try:
        temp_chatbot = ChatbotBackend()
        if temp_chatbot.project_data:
            project_info = {
                "loaded": True,
                "title": temp_chatbot.project_data.get('title', 'Unknown'),
                "brief_length": len(temp_chatbot.project_data.get('brief', ''))
            }
    except Exception:
        pass
    
    # Get conversation summaries
    conversation_summaries = []
    for conv_id, chatbot in chatbot_instances.items():
        summary = chatbot.get_conversation_summary()
        conversation_summaries.append({
            "conversation_id": conv_id,
            "message_count": summary["message_count"],
            "tools_enabled": chatbot.enable_tools,
            "last_message_at": summary.get("last_message_at")
        })
    
    return {
        "status": "Chatbot services available",
        "active_conversations": len(chatbot_instances),
        "project_info": project_info,
        "conversations": conversation_summaries,
        "services": ["conversation_management", "ai_chat", "tool_calling"],
        "claude_model": "claude-sonnet-4-20250514"
    }

@app.post("/chatbot/conversations", response_model=ChatbotCreateResponse)
async def create_chatbot_conversation(request: ChatbotCreateRequest):
    """
    Create a new chatbot conversation
    
    Creates a new chatbot instance with optional conversation ID and tool settings.
    """
    if ChatbotBackend is None:
        raise HTTPException(status_code=503, detail="Chatbot services not available")
    
    try:
        # Create new chatbot instance
        chatbot = ChatbotBackend(
            conversation_id=request.conversation_id,
            enable_tools=request.enable_tools
        )
        
        # Store in global tracking
        chatbot_instances[chatbot.conversation_id] = chatbot
        
        # Get welcome message
        welcome_message = chatbot.get_welcome_message()
        
        return ChatbotCreateResponse(
            conversation_id=chatbot.conversation_id,
            welcome_message=welcome_message,
            tools_enabled=request.enable_tools,
            created_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create chatbot conversation: {str(e)}")

@app.get("/chatbot/conversations")
async def list_chatbot_conversations():
    """
    List all active chatbot conversations
    
    Returns a list of all currently active chatbot instances.
    """
    conversations = []
    
    for conv_id, chatbot in chatbot_instances.items():
        summary = chatbot.get_conversation_summary()
        conversations.append(ChatbotConversationInfo(
            conversation_id=conv_id,
            message_count=summary["message_count"],
            created_at=summary.get("created_at"),
            last_message_at=summary.get("last_message_at"),
            tools_enabled=chatbot.enable_tools
        ))
    
    return {
        "active_conversations": len(conversations),
        "conversations": conversations
    }

@app.get("/chatbot/conversations/{conversation_id}")
async def get_chatbot_conversation(conversation_id: str):
    """
    Get details about a specific chatbot conversation
    """
    if conversation_id not in chatbot_instances:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    
    chatbot = chatbot_instances[conversation_id]
    summary = chatbot.get_conversation_summary()
    
    return ChatbotConversationInfo(
        conversation_id=conversation_id,
        message_count=summary["message_count"],
        created_at=summary.get("created_at"),
        last_message_at=summary.get("last_message_at"),
        tools_enabled=chatbot.enable_tools
    )

@app.get("/chatbot/conversations/{conversation_id}/welcome", response_model=ChatbotWelcomeResponse)
async def get_chatbot_welcome(conversation_id: str):
    """
    Get the welcome message for a specific conversation
    """
    if ChatbotBackend is None:
        raise HTTPException(status_code=503, detail="Chatbot services not available")
    
    if conversation_id not in chatbot_instances:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    
    chatbot = chatbot_instances[conversation_id]
    welcome_message = chatbot.get_welcome_message()
    
    return ChatbotWelcomeResponse(
        welcome_message=welcome_message,
        conversation_id=conversation_id
    )

@app.post("/chatbot/conversations/{conversation_id}/tools/toggle", response_model=ChatbotToggleToolsResponse)
async def toggle_chatbot_tools(conversation_id: str, request: ChatbotToggleToolsRequest):
    """
    Toggle tools on/off for a chatbot conversation
    
    Enables or disables tool usage for the specified conversation.
    """
    if ChatbotBackend is None:
        raise HTTPException(status_code=503, detail="Chatbot services not available")
    
    if conversation_id not in chatbot_instances:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    
    chatbot = chatbot_instances[conversation_id]
    chatbot.enable_tools = request.enable_tools
    
    status_message = "enabled" if request.enable_tools else "disabled"
    
    return ChatbotToggleToolsResponse(
        conversation_id=conversation_id,
        tools_enabled=request.enable_tools,
        message=f"Tools are now {status_message} for conversation {conversation_id}"
    )

@app.get("/chatbot/project", response_model=ChatbotProjectInfoResponse)
async def get_chatbot_project_info():
    """
    Get current project information available to chatbots
    
    Returns information about the loaded project data including title and brief.
    """
    if ChatbotBackend is None:
        raise HTTPException(status_code=503, detail="Chatbot services not available")
    
    try:
        # Create a temporary chatbot instance to get project data
        temp_chatbot = ChatbotBackend()
        
        if not temp_chatbot.project_data:
            return ChatbotProjectInfoResponse(
                project_loaded=False,
                project_title=None,
                brief_length=None,
                brief_preview=None
            )
        
        project_data = temp_chatbot.project_data
        brief = project_data.get('brief', '')
        brief_preview = brief[:200] + "..." if len(brief) > 200 else brief if brief else None
        
        return ChatbotProjectInfoResponse(
            project_loaded=True,
            project_title=project_data.get('title', 'Unknown'),
            brief_length=len(brief),
            brief_preview=brief_preview
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get project info: {str(e)}")

@app.post("/chatbot/conversations/{conversation_id}/restart")
async def restart_chatbot_conversation(conversation_id: str):
    """
    Restart a chatbot conversation
    
    Clears the conversation history and reinitializes the chatbot instance.
    """
    if ChatbotBackend is None:
        raise HTTPException(status_code=503, detail="Chatbot services not available")
    
    if conversation_id not in chatbot_instances:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    
    try:
        # Get current settings
        old_chatbot = chatbot_instances[conversation_id]
        enable_tools = old_chatbot.enable_tools
        
        # Create new chatbot instance with same ID and settings
        new_chatbot = ChatbotBackend(
            conversation_id=conversation_id,
            enable_tools=enable_tools
        )
        
        # Replace in global tracking
        chatbot_instances[conversation_id] = new_chatbot
        
        # Get welcome message
        welcome_message = new_chatbot.get_welcome_message()
        
        return {
            "message": f"Conversation {conversation_id} restarted successfully",
            "conversation_id": conversation_id,
            "tools_enabled": enable_tools,
            "welcome_message": welcome_message,
            "restarted_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restart conversation: {str(e)}")

@app.delete("/chatbot/conversations/{conversation_id}")
async def delete_chatbot_conversation(conversation_id: str):
    """
    Delete a chatbot conversation
    
    Removes the conversation from active instances.
    """
    if conversation_id not in chatbot_instances:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    
    del chatbot_instances[conversation_id]
    
    return {"message": f"Conversation {conversation_id} deleted successfully"}

@app.post("/chatbot/conversations/{conversation_id}/clear")
async def clear_chatbot_conversation(conversation_id: str):
    """
    Clear the history of a chatbot conversation
    
    Clears the conversation history while keeping the instance active.
    """
    if conversation_id not in chatbot_instances:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    
    chatbot = chatbot_instances[conversation_id]
    chatbot.clear_conversation()
    
    return {"message": f"Conversation {conversation_id} history cleared"}

@app.post("/chatbot/conversations/{conversation_id}/message")
async def send_chatbot_message_sync(conversation_id: str, request: ChatbotMessageRequest):
    """
    Send a message to the chatbot (synchronous response)
    
    Sends a message and returns the complete response including thinking and tool calls.
    """
    if ChatbotBackend is None:
        raise HTTPException(status_code=503, detail="Chatbot services not available")
    
    if conversation_id not in chatbot_instances:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    
    try:
        chatbot = chatbot_instances[conversation_id]
        
        # Send message to chatbot
        result = chatbot.send_message(request.message)
        
        if result.get("success"):
            return ChatbotMessageResponse(
                success=True,
                response=result.get("response"),
                thinking=result.get("thinking"),
                tool_calls=result.get("tool_calls", []),
                conversation_id=conversation_id,
                message_count=result.get("message_count", 0)
            )
        else:
            return ChatbotMessageResponse(
                success=False,
                error=result.get("error"),
                conversation_id=conversation_id,
                message_count=0
            )
            
    except Exception as e:
        return ChatbotMessageResponse(
            success=False,
            error=str(e),
            conversation_id=conversation_id,
            message_count=0
        )

@app.post("/chatbot/conversations/{conversation_id}/message/stream")
async def send_chatbot_message_stream(conversation_id: str, request: ChatbotMessageRequest):
    """
    Send a message to the chatbot (streaming response)
    
    Sends a message and streams the response in real-time including thinking and tool execution.
    """
    if ChatbotBackend is None:
        raise HTTPException(status_code=503, detail="Chatbot services not available")
    
    if conversation_id not in chatbot_instances:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    
    chatbot = chatbot_instances[conversation_id]
    
    async def generate_stream():
        """Generate Server-Sent Events for streaming response"""
        
        # Track the streaming content
        streaming_data = {
            "thinking": "",
            "response": "",
            "tool_calls": [],
            "error": None
        }
        
        # Store streaming events to send them out
        streaming_events = []
        
        def streaming_callback(stream_type: str, content: str):
            """Callback to capture streaming content"""
            nonlocal streaming_data, streaming_events
            
            print(f"Streaming callback: {stream_type} - {content[:100]}...")  # Debug log
            
            if stream_type == "thinking":
                streaming_data["thinking"] += content
                event_data = {
                    "type": "thinking",
                    "content": content,
                    "conversation_id": conversation_id
                }
                streaming_events.append(f"data: {json.dumps(event_data)}\n\n")
            
            elif stream_type == "tool":
                event_data = {
                    "type": "tool",
                    "content": content,
                    "conversation_id": conversation_id
                }
                streaming_events.append(f"data: {json.dumps(event_data)}\n\n")
            
            elif stream_type == "response":
                streaming_data["response"] += content
                event_data = {
                    "type": "response",
                    "content": content,
                    "conversation_id": conversation_id
                }
                streaming_events.append(f"data: {json.dumps(event_data)}\n\n")
        
        try:
            # Send start event
            yield f"data: {json.dumps({'type': 'start', 'conversation_id': conversation_id})}\n\n"
            
            # Send message to chatbot with streaming callback
            print(f"Sending message to chatbot: {request.message}")
            result = chatbot.send_message(request.message, streaming_callback=streaming_callback)
            
            print(f"Chatbot result: success={result.get('success')}, tool_calls={len(result.get('tool_calls', []))}")
            print(f"Collected {len(streaming_events)} streaming events")
            
            # Send all collected streaming events first
            for event in streaming_events:
                yield event
            
            # Send completion event
            completion_data = {
                "type": "complete",
                "success": result.get("success", False),
                "conversation_id": conversation_id,
                "message_count": result.get("message_count", 0),
                "tool_calls": result.get("tool_calls", [])
            }
            
            if not result.get("success"):
                completion_data["error"] = result.get("error")
            
            yield f"data: {json.dumps(completion_data)}\n\n"
            
        except Exception as e:
            # Send error event
            error_data = {
                "type": "error",
                "error": str(e),
                "conversation_id": conversation_id
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )

@app.get("/chatbot/tools")
async def list_chatbot_tools():
    """
    List all available chatbot tools
    
    Returns information about all tools that can be used by the chatbot.
    """
    if ChatbotBackend is None:
        raise HTTPException(status_code=503, detail="Chatbot services not available")
    
    try:
        # Create a temporary chatbot instance to get tools
        temp_chatbot = ChatbotBackend()
        tools = temp_chatbot.list_available_tools()
        
        return {
            "available_tools": len(tools),
            "tools": tools
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list tools: {str(e)}")

@app.post("/chatbot/conversations/{conversation_id}/tools", response_model=ChatbotToolResponse)
async def call_chatbot_tool(conversation_id: str, request: ChatbotToolRequest):
    """
    Manually call a chatbot tool
    
    Allows manual execution of tools for testing purposes.
    """
    if ChatbotBackend is None:
        raise HTTPException(status_code=503, detail="Chatbot services not available")
    
    if conversation_id not in chatbot_instances:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    
    try:
        chatbot = chatbot_instances[conversation_id]
        result = chatbot.call_tool_manually(request.tool_name, request.parameters)
        
        return ChatbotToolResponse(
            success=result.get("success", False),
            tool_name=request.tool_name,
            result=result.get("result") if result.get("success") else None,
            error=result.get("error") if not result.get("success") else None
        )
        
    except Exception as e:
        return ChatbotToolResponse(
            success=False,
            tool_name=request.tool_name,
            error=str(e)
        )

async def process_analysis_job(job_id: str):
    """
    Background task to process video analysis job with detailed progress updates
    """
    def update_progress(message: str, status: str = "processing"):
        """Helper function to update job progress"""
        analysis_jobs[job_id]["progress"] = message
        analysis_jobs[job_id]["message"] = message
        if status != "processing":
            analysis_jobs[job_id]["status"] = status
    
    try:
        # Update job status
        analysis_jobs[job_id]["status"] = "processing"
        update_progress("Initializing video analyzer...")
        
        # Get job parameters
        job_data = analysis_jobs[job_id]
        
        # Add services path for imports
        services_path = os.path.join(os.path.dirname(__file__), "services", "assetanalysis")
        if services_path not in sys.path:
            sys.path.insert(0, services_path)
        
        # Import and initialize VideoAnalyzer
        from services.assetanalysis.videoanalyzer import VideoAnalyzer
        
        update_progress("Loading video analyzer...")
        
        # Create a custom analyzer with progress callback
        class ProgressVideoAnalyzer(VideoAnalyzer):
            def _poll_transcription(self, transcript_id: str):
                """Override polling with progress updates"""
                import time
                import requests
                
                polling_endpoint = f"{self.BASE_URL}/transcript/{transcript_id}"
                start_time = time.time()
                
                while True:
                    try:
                        response = requests.get(polling_endpoint, headers=self.headers, timeout=30)
                        response.raise_for_status()
                        result = response.json()
                        
                        status = result["status"]
                        elapsed = time.time() - start_time
                        
                        # Update progress based on AssemblyAI status
                        if status == "queued":
                            update_progress(f"AssemblyAI: Transcription queued (elapsed: {elapsed:.0f}s)")
                        elif status == "processing":
                            update_progress(f"AssemblyAI: Transcribing audio (elapsed: {elapsed:.0f}s)")
                        elif status == "completed":
                            update_progress("AssemblyAI: Transcription completed, processing results...")
                            return result
                        elif status == "error":
                            error_msg = result.get('error', 'Unknown error')
                            raise RuntimeError(f"AssemblyAI transcription failed: {error_msg}")
                        
                        # Progressive backoff
                        wait_time = min(5 + (elapsed // 60), 15)
                        time.sleep(wait_time)
                        
                    except requests.RequestException as e:
                        update_progress(f"AssemblyAI: Transcription in progress (connection retry)")
                        time.sleep(10)
        
        analyzer = ProgressVideoAnalyzer(brief_path=job_data["brief_path"])
        
        update_progress("Analyzing video file...")
        
        # Override the analyzer's progress methods
        original_probe = analyzer.probe_video_file
        original_extract = analyzer.extract_audio
        original_upload = analyzer.upload_audio_file
        original_transcribe = analyzer.transcribe_audio
        original_process = analyzer.process_transcript_to_words
        
        def probe_with_progress(file_path):
            update_progress("Step 1/5: Reading video metadata...")
            return original_probe(file_path)
        
        def extract_with_progress(video_path):
            update_progress("Step 2/5: Extracting audio from video...")
            return original_extract(video_path)
        
        def upload_with_progress(audio_file_path):
            update_progress("Step 3/5: Uploading audio to AssemblyAI...")
            return original_upload(audio_file_path)
        
        def transcribe_with_progress(audio_url, custom_spell=None):
            update_progress("Step 4/5: Starting AssemblyAI transcription...")
            return original_transcribe(audio_url, custom_spell)
        
        def process_with_progress(transcript_data, fps, timecode_offset_frames=0, silence_threshold_ms=1000):
            update_progress("Step 5/5: Processing transcript results...")
            return original_process(transcript_data, fps, timecode_offset_frames, silence_threshold_ms)
        
        # Monkey patch the methods
        analyzer.probe_video_file = probe_with_progress
        analyzer.extract_audio = extract_with_progress
        analyzer.upload_audio_file = upload_with_progress
        analyzer.transcribe_audio = transcribe_with_progress
        analyzer.process_transcript_to_words = process_with_progress
        
        # Process the video with progress updates
        result = analyzer.analyze(
            video_path=job_data["video_path"],
            output_path=None,  # Force using data/analyzed directory
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
        
        # The output file path is determined by VideoAnalyzer.analyze() 
        # It should now go to data/analyzed directory
        video_filename = Path(job_data["video_path"]).stem
        analyzed_dir = Path(__file__).parent.parent.parent / "data" / "analyzed"
        output_file = str(analyzed_dir / f"{video_filename}.transcript.json")
        
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
    
    if ChatbotBackend is not None:
        print("  - AI Chatbot:")
        print("    - Status: GET /chatbot/status")
        print("    - Project Info: GET /chatbot/project")
        print("    - Create Conversation: POST /chatbot/conversations")
        print("    - List Conversations: GET /chatbot/conversations")
        print("    - Get Conversation: GET /chatbot/conversations/{id}")
        print("    - Get Welcome Message: GET /chatbot/conversations/{id}/welcome")
        print("    - Send Message (Sync): POST /chatbot/conversations/{id}/message")
        print("    - Send Message (Stream): POST /chatbot/conversations/{id}/message/stream")
        print("    - Clear Conversation: POST /chatbot/conversations/{id}/clear")
        print("    - Restart Conversation: POST /chatbot/conversations/{id}/restart")
        print("    - Delete Conversation: DELETE /chatbot/conversations/{id}")
        print("    - Toggle Tools: POST /chatbot/conversations/{id}/tools/toggle")
        print("    - List Tools: GET /chatbot/tools")
        print("    - Call Tool: POST /chatbot/conversations/{id}/tools")
    else:
        print("  - AI Chatbot: Not available (missing dependencies)")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )

if __name__ == "__main__":
    main()
