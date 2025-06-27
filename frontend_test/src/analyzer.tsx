import React, { useState, useEffect, useCallback } from 'react';
import './styles.css';

interface AnalysisJob {
  job_id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  message: string;
  progress?: string;
  created_at: string;
  completed_at?: string;
  result?: any;
  error?: string;
  output_file?: string;
}

interface ApiStatus {
  status: string;
  isConnected: boolean;
  error?: string;
}

const VideoAnalyzer: React.FC = () => {
  // State management
  const [apiStatus, setApiStatus] = useState<ApiStatus>({ status: 'Checking...', isConnected: false });
  const [selectedFile, setSelectedFile] = useState<string>('');
  const [silenceThreshold, setSilenceThreshold] = useState<number>(1000);
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const [statusLog, setStatusLog] = useState<string>('Ready to analyze video files...\n');
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);

  const API_BASE_URL = 'http://127.0.0.1:8000';

  // API Status Check
  const checkApiStatus = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (response.ok) {
        const data = await response.json();
        setApiStatus({
          status: `✅ Connected - ${data.status}`,
          isConnected: true
        });
      } else {
        setApiStatus({
          status: `❌ API Error (${response.status})`,
          isConnected: false
        });
      }
    } catch (error) {
      setApiStatus({
        status: '❌ FastAPI Server Not Running',
        isConnected: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }, []);

  // Log message to status display
  const logMessage = useCallback((message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = `[${timestamp}] ${message}\n`;
    setStatusLog(prev => prev + logEntry);
  }, []);

  // File selection handlers
  const handleFileSelect = () => {
    // In Electron, you'd use the main process to open file dialog
    // For now, we'll use the web file input as fallback
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'video/*';
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        setSelectedFile(file.path || file.name);
        logMessage(`Selected file: ${file.name}`);
      }
    };
    input.click();
  };

  // Drag and drop handlers
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    const files = Array.from(e.dataTransfer.files);
    const videoFile = files.find(file => file.type.startsWith('video/'));
    
    if (videoFile) {
      setSelectedFile(videoFile.path || videoFile.name);
      logMessage(`Dropped file: ${videoFile.name}`);
    } else {
      logMessage('⚠️ Please drop a video file');
    }
  };

  // Start analysis
  const startAnalysis = async () => {
    if (!selectedFile || !apiStatus.isConnected) {
      logMessage('❌ Cannot start analysis: No file selected or API not connected');
      return;
    }

    setIsAnalyzing(true);
    logMessage('🚀 Starting video analysis...');

    try {
      const response = await fetch(`${API_BASE_URL}/analysis/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_path: selectedFile,
          silence_threshold_ms: silenceThreshold
        })
      });

      if (response.ok) {
        const data = await response.json();
        setCurrentJobId(data.job_id);
        logMessage(`✅ Analysis job created: ${data.job_id}`);
        logMessage(`📝 Status: ${data.message}`);
        
        // Start polling for status
        pollJobStatus(data.job_id);
      } else {
        const errorData = await response.json();
        logMessage(`❌ Failed to start analysis: ${errorData.detail || 'Unknown error'}`);
        setIsAnalyzing(false);
      }
    } catch (error) {
      logMessage(`❌ Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
      setIsAnalyzing(false);
    }
  };

  // Poll job status
  const pollJobStatus = async (jobId: string) => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/analysis/status/${jobId}`);
        
        if (response.ok) {
          const job: AnalysisJob = await response.json();
          
          // Update status log
          if (job.progress) {
            logMessage(`📊 ${job.progress}`);
          }
          
          // Check if job is complete
          if (job.status === 'completed') {
            clearInterval(pollInterval);
            setIsAnalyzing(false);
            setCurrentJobId(null);
            
            logMessage('🎉 Analysis completed successfully!');
            if (job.output_file) {
              logMessage(`💾 Output saved to: ${job.output_file}`);
            }
            
            // Display results summary
            if (job.result) {
              const result = job.result;
              logMessage('📋 Results Summary:');
              logMessage(`   • File: ${result.file_name || 'N/A'}`);
              logMessage(`   • FPS: ${result.fps || 'N/A'}`);
              logMessage(`   • Duration: ${result.duration_frames || 'N/A'} frames`);
              logMessage(`   • Speakers: ${result.speakers?.join(', ') || 'None detected'}`);
              
              const words = result.words || [];
              const wordCount = words.filter((w: any) => w.word !== '**SILENCE**').length;
              const silenceCount = words.filter((w: any) => w.word === '**SILENCE**').length;
              
              logMessage(`   • Words: ${wordCount}`);
              logMessage(`   • Silence periods: ${silenceCount}`);
            }
            
          } else if (job.status === 'failed') {
            clearInterval(pollInterval);
            setIsAnalyzing(false);
            setCurrentJobId(null);
            
            logMessage(`❌ Analysis failed: ${job.error || job.message}`);
          }
        } else {
          logMessage('⚠️ Failed to get job status');
        }
      } catch (error) {
        logMessage(`⚠️ Status check error: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    }, 2000); // Poll every 2 seconds

    // Cleanup after 10 minutes
    setTimeout(() => {
      clearInterval(pollInterval);
      if (isAnalyzing) {
        logMessage('⏰ Status polling timed out');
        setIsAnalyzing(false);
      }
    }, 600000);
  };

  // Copy status to clipboard
  const copyStatusToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(statusLog);
      logMessage('📋 Status copied to clipboard');
    } catch (error) {
      logMessage('❌ Failed to copy to clipboard');
    }
  };

  // Clear status log
  const clearStatusLog = () => {
    setStatusLog('Status log cleared.\n');
  };

  // Effects
  useEffect(() => {
    checkApiStatus();
    const interval = setInterval(checkApiStatus, 5000);
    return () => clearInterval(interval);
  }, [checkApiStatus]);

  return (
    <div className="analyzer-container">
      <div className="analyzer-header">
        <h1>🎬 Video Analysis Test UI</h1>
        <p>Electron-based test interface for video analysis API</p>
      </div>

      {/* API Status Section */}
      <div className="section api-status">
        <div className="section-header">
          <h3>API Status</h3>
          <button onClick={checkApiStatus} className="btn-small">
            🔄 Refresh
          </button>
        </div>
        <div className="status-display">
          <span className={`status-indicator ${apiStatus.isConnected ? 'connected' : 'disconnected'}`}>
            {apiStatus.status}
          </span>
        </div>
      </div>

      {/* File Selection Section */}
      <div 
        className="section file-selection"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <div className="section-header">
          <h3>File Selection</h3>
          <button onClick={handleFileSelect} className="btn-primary" disabled={isAnalyzing}>
            📁 Browse
          </button>
        </div>
        <div className="file-display">
          <span className="file-path">
            {selectedFile || 'No file selected (drag & drop or browse)'}
          </span>
        </div>
        <div className="hint">
          💡 Tip: You can drag & drop video files directly onto this section
        </div>
      </div>

      {/* Analysis Controls Section */}
      <div className="section analysis-controls">
        <div className="section-header">
          <h3>Analysis Settings</h3>
          <button 
            onClick={startAnalysis} 
            className="btn-success"
            disabled={!selectedFile || !apiStatus.isConnected || isAnalyzing}
          >
            {isAnalyzing ? '⏳ Analyzing...' : '🚀 Start Analysis'}
          </button>
        </div>
        <div className="controls-row">
          <label htmlFor="silence-threshold">Silence Threshold (ms):</label>
          <input
            id="silence-threshold"
            type="number"
            value={silenceThreshold}
            onChange={(e) => setSilenceThreshold(parseInt(e.target.value) || 1000)}
            min="100"
            max="10000"
            step="100"
            disabled={isAnalyzing}
          />
        </div>
      </div>

      {/* Status Display Section */}
      <div className="section status-section">
        <div className="section-header">
          <h3>Status & Progress</h3>
          <div className="status-controls">
            <button onClick={copyStatusToClipboard} className="btn-small">
              📋 Copy
            </button>
            <button onClick={clearStatusLog} className="btn-small">
              🗑️ Clear
            </button>
          </div>
        </div>
        <div className="status-log">
          <pre>{statusLog}</pre>
        </div>
      </div>

      {/* Current Job Info */}
      {currentJobId && (
        <div className="section job-info">
          <div className="section-header">
            <h3>Current Job</h3>
          </div>
          <div className="job-details">
            <span>Job ID: {currentJobId}</span>
            <span className="job-status">Status: Processing</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default VideoAnalyzer;
