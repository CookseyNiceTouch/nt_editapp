import React, { useState, useEffect, useCallback } from 'react';
import './styles.css';

interface ApiStatus {
  status: string;
  isConnected: boolean;
  active_conversations?: number;
  project_info?: {
    loaded: boolean;
    title?: string;
    brief_length?: number;
  };
  conversations?: Array<{
    conversation_id: string;
    message_count: number;
    tools_enabled: boolean;
    last_message_at?: string;
  }>;
  claude_model?: string;
  error?: string;
}

interface ProjectInfo {
  project_loaded: boolean;
  project_title?: string;
  brief_length?: number;
  brief_preview?: string;
}

interface Tool {
  name: string;
  description: string;
  parameters?: any;
}

const ProjectManager: React.FC = () => {
  // State management
  const [apiStatus, setApiStatus] = useState<ApiStatus>({ status: 'Checking...', isConnected: false });
  const [projectInfo, setProjectInfo] = useState<ProjectInfo | null>(null);
  const [availableTools, setAvailableTools] = useState<Tool[]>([]);

  const API_BASE_URL = 'http://127.0.0.1:8000';

  // API Status Check
  const checkApiStatus = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/status`);
      if (response.ok) {
        const data = await response.json();
        setApiStatus({
          status: `✅ Connected - ${data.status}`,
          isConnected: true,
          active_conversations: data.active_conversations,
          project_info: data.project_info,
          conversations: data.conversations,
          claude_model: data.claude_model
        });
      } else {
        setApiStatus({
          status: `❌ API Error (${response.status})`,
          isConnected: false
        });
      }
    } catch (error) {
      setApiStatus({
        status: '❌ Chatbot API Not Available',
        isConnected: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }, []);

  // Load project information
  const loadProjectInfo = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/project`);
      if (response.ok) {
        const data = await response.json();
        setProjectInfo(data);
      }
    } catch (error) {
      console.error('Failed to load project info:', error);
    }
  }, []);

  // Load available tools
  const loadAvailableTools = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/tools`);
      if (response.ok) {
        const data = await response.json();
        setAvailableTools(data.tools || []);
      }
    } catch (error) {
      console.error('Failed to load tools:', error);
    }
  }, []);

  // Effects
  useEffect(() => {
    checkApiStatus();
    loadProjectInfo();
    loadAvailableTools();
    
    const interval = setInterval(() => {
      checkApiStatus();
    }, 10000);
    
    return () => clearInterval(interval);
  }, [checkApiStatus, loadProjectInfo, loadAvailableTools]);

  return (
    <div className="project-manager-container">
      <div className="project-manager-header">
        <h1>🎬 Project Manager</h1>
        <p>System status and project information</p>
      </div>

      {/* API Status */}
      <div className="section api-status">
        <div className="section-header">
          <h3>🔌 API Status</h3>
          <button onClick={checkApiStatus} className="btn-small">
            🔄 Refresh
          </button>
        </div>
        <div className="status-display">
          <span className={`status-indicator ${apiStatus.isConnected ? 'connected' : 'disconnected'}`}>
            {apiStatus.status}
          </span>
          {apiStatus.active_conversations !== undefined && (
            <span className="conversation-count">
              Active conversations: {apiStatus.active_conversations}
            </span>
          )}
          {apiStatus.claude_model && (
            <span className="conversation-count">
              Model: {apiStatus.claude_model}
            </span>
          )}
        </div>
        
        {/* Enhanced Status Details */}
        {apiStatus.isConnected && apiStatus.project_info && (
          <div className="status-details">
            <h4>📁 Project Status</h4>
            <div className="project-status">
              <span className={`project-indicator ${apiStatus.project_info.loaded ? 'loaded' : 'not-loaded'}`}>
                {apiStatus.project_info.loaded ? '✅ Project Loaded' : '❌ No Project'}
              </span>
              {apiStatus.project_info.loaded && (
                <>
                  <span className="project-title">Title: {apiStatus.project_info.title || 'Unknown'}</span>
                  <span className="brief-length">Brief: {apiStatus.project_info.brief_length || 0} characters</span>
                </>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Project Information */}
      {projectInfo && (
        <div className="section project-info">
          <div className="section-header">
            <h3>📁 Project Information</h3>
            <button onClick={loadProjectInfo} className="btn-small">
              🔄 Refresh
            </button>
          </div>
          
          {projectInfo.project_loaded ? (
            <div className="project-details">
              <div><strong>Title:</strong> {projectInfo.project_title || 'Unknown'}</div>
              <div><strong>Brief Length:</strong> {projectInfo.brief_length || 0} characters</div>
              {projectInfo.brief_preview && (
                <div className="brief-preview">
                  <strong>Brief Preview:</strong>
                  <pre>{projectInfo.brief_preview}</pre>
                </div>
              )}
            </div>
          ) : (
            <div className="no-project">❌ No project data loaded</div>
          )}
        </div>
      )}

      {/* System Information */}
      {apiStatus.isConnected && (
        <div className="section system-info">
          <div className="section-header">
            <h3>⚙️ System Information</h3>
          </div>
          
          <div className="system-details">
            <div className="system-row">
              <span className="system-label">Backend Status:</span>
              <span className="system-value connected">✅ Online</span>
            </div>
            <div className="system-row">
              <span className="system-label">AI Model:</span>
              <span className="system-value">{apiStatus.claude_model || 'Unknown'}</span>
            </div>
            <div className="system-row">
              <span className="system-label">Available Tools:</span>
              <span className="system-value">{availableTools.length} tools loaded</span>
            </div>
            {apiStatus.conversations && apiStatus.conversations.length > 0 && (
              <div className="system-row">
                <span className="system-label">Active Conversations:</span>
                <span className="system-value">{apiStatus.conversations.length}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Available Tools */}
      <div className="section tools-panel">
        <div className="section-header">
          <h3>🔧 Available Tools</h3>
          <button onClick={loadAvailableTools} className="btn-small">
            🔄 Refresh
          </button>
        </div>
        
        <div className="tools-list">
          {availableTools.length === 0 ? (
            <div className="no-tools">No tools available</div>
          ) : (
            availableTools.map(tool => (
              <div key={tool.name} className="tool-item">
                <div className="tool-name">{tool.name}</div>
                <div className="tool-description">{tool.description}</div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default ProjectManager;
