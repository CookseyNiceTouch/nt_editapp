import { useState, useEffect } from 'react'
import LogViewer from './LogViewer'

interface AnalyzedFile {
  file_name: string
  original_video: string
  analyzed_at: string
  file_size: number
  speakers: string[]
  duration_frames: number
  fps: number
  word_count: number
  silence_count: number
}

interface JobStatus {
  id: string
  status: string
  file_name: string
  progress: number
  created_at: string
  updated_at?: string
  error?: string
}

interface QueueStatus {
  queued_jobs: JobStatus[]
  active_jobs: JobStatus[]
  queue_length: number
  is_processing: boolean
}

interface FootageIngestProps {
  // No props needed for now, but we can add them later if needed
}

const API_BASE_URL = 'http://localhost:8001'

export default function FootageIngest({}: FootageIngestProps) {
  const [isDragOver, setIsDragOver] = useState(false)
  const [analyzedFiles, setAnalyzedFiles] = useState<AnalyzedFile[]>([])
  const [queueStatus, setQueueStatus] = useState<QueueStatus | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showLogs, setShowLogs] = useState(false)

  // Fetch analyzed files and queue status
  useEffect(() => {
    fetchAnalyzedFiles()
    fetchQueueStatus()
    
    // Poll queue status every 2 seconds
    const interval = setInterval(fetchQueueStatus, 2000)
    return () => clearInterval(interval)
  }, [])

  // Auto-show logs when processing starts
  useEffect(() => {
    if (queueStatus?.is_processing && !showLogs) {
      setShowLogs(true)
    }
  }, [queueStatus?.is_processing, showLogs])

  const fetchAnalyzedFiles = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/analyzed`)
      if (response.ok) {
        const files = await response.json()
        setAnalyzedFiles(files)
      } else {
        console.error('Failed to fetch analyzed files:', response.statusText)
      }
    } catch (error) {
      console.error('Error fetching analyzed files:', error)
    }
  }

  const fetchQueueStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/queue`)
      if (response.ok) {
        const status = await response.json()
        setQueueStatus(status)
      } else {
        console.error('Failed to fetch queue status:', response.statusText)
      }
    } catch (error) {
      console.error('Error fetching queue status:', error)
    }
  }

  const uploadFiles = async (files: File[]) => {
    setIsLoading(true)
    setError(null)

    for (const file of files) {
      try {
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch(`${API_BASE_URL}/upload`, {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Upload failed')
        }

        const result = await response.json()
        console.log(`File ${file.name} uploaded successfully:`, result)
      } catch (error) {
        console.error(`Error uploading ${file.name}:`, error)
        setError(`Failed to upload ${file.name}: ${error}`)
      }
    }

    setIsLoading(false)
    // Refresh queue status after uploads
    fetchQueueStatus()
  }

  const deleteAnalyzedFile = async (fileName: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/analyzed/${fileName}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        // Refresh analyzed files list
        fetchAnalyzedFiles()
      } else {
        const errorData = await response.json()
        setError(`Failed to delete file: ${errorData.detail}`)
      }
    } catch (error) {
      console.error('Error deleting file:', error)
      setError(`Error deleting file: ${error}`)
    }
  }

  const cancelJob = async (jobId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/queue/${jobId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        fetchQueueStatus()
      } else {
        const errorData = await response.json()
        setError(`Failed to cancel job: ${errorData.detail}`)
      }
    } catch (error) {
      console.error('Error cancelling job:', error)
      setError(`Error cancelling job: ${error}`)
    }
  }

  const clearQueue = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/queue`, {
        method: 'DELETE'
      })

      if (response.ok) {
        fetchQueueStatus()
      } else {
        const errorData = await response.json()
        setError(`Failed to clear queue: ${errorData.detail}`)
      }
    } catch (error) {
      console.error('Error clearing queue:', error)
      setError(`Error clearing queue: ${error}`)
    }
  }

  const viewTranscript = async (fileName: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/analyzed/${fileName}`)
      if (response.ok) {
        const data = await response.json()
        // TODO: Open transcript viewer modal or new window
        console.log('Transcript data:', data)
        // For now, just log it
        alert(`Transcript for ${fileName} logged to console`)
      } else {
        setError('Failed to fetch transcript')
      }
    } catch (error) {
      console.error('Error fetching transcript:', error)
      setError(`Error fetching transcript: ${error}`)
    }
  }

  // Handle drag events
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
    
    const files = Array.from(e.dataTransfer.files).filter(file => 
      file.type.startsWith('video/') || file.type.startsWith('audio/')
    )
    
    if (files.length > 0) {
      uploadFiles(files)
    }
  }

  // Handle file input
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    if (files.length > 0) {
      uploadFiles(files)
    }
    // Reset input
    e.target.value = ''
  }

  const openImportDialog = () => {
    document.getElementById('file-input')?.click()
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDuration = (frames: number, fps: number) => {
    const seconds = frames / fps
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = Math.floor(seconds % 60)
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleString()
    } catch {
      return dateString
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return '✅'
      case 'processing': return '⏳'
      case 'queued': return '⏸️'
      case 'error': return '❌'
      case 'cancelling': return '🛑'
      default: return '📄'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed': return 'Completed'
      case 'processing': return 'Processing...'
      case 'queued': return 'Queued'
      case 'error': return 'Error'
      case 'cancelling': return 'Cancelling...'
      default: return status
    }
  }

  const allJobs = [
    ...(queueStatus?.queued_jobs || []),
    ...(queueStatus?.active_jobs || [])
  ]

  return (
    <>
      <div className="footage-panel">
        {/* Error Display */}
        {error && (
          <div className="error-banner">
            <span>⚠️ {error}</span>
            <button onClick={() => setError(null)}>✕</button>
          </div>
        )}

        {/* File Drop Zone */}
        <section className="file-upload-section">
          <h2>Import Footage</h2>
          <div 
            className={`drop-zone ${isDragOver ? 'drag-over' : ''} ${isLoading ? 'loading' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <div className="drop-zone-content">
              <div className="drop-icon">📁</div>
              <p className="drop-text">
                {isLoading ? 'Uploading files...' : 'Drag and drop your video/audio files here'}
              </p>
              <p className="drop-subtext">
                or
              </p>
              <button 
                className="import-button" 
                onClick={openImportDialog}
                disabled={isLoading}
              >
                {isLoading ? 'Uploading...' : 'Browse Files'}
              </button>
              <input
                type="file"
                multiple
                accept="video/*,audio/*"
                onChange={handleFileSelect}
                className="hidden-file-input"
                id="file-input"
                disabled={isLoading}
              />
            </div>
          </div>
          <p className="file-types-hint">
            Supported formats: MP4, AVI, MOV, MKV, WMV, FLV, WebM
          </p>
        </section>

        {/* Queue Status */}
        {queueStatus && (allJobs.length > 0 || queueStatus.is_processing) && (
          <section className="queue-section">
            <div className="queue-header">
              <h2>Processing Queue ({queueStatus.queue_length})</h2>
              <div className="queue-header-actions">
                {queueStatus.queue_length > 0 && (
                  <button className="clear-queue-button" onClick={clearQueue}>
                    Clear Queue
                  </button>
                )}
                <button 
                  className="log-toggle-button" 
                  onClick={() => setShowLogs(!showLogs)}
                  style={{ marginLeft: '0.5rem' }}
                >
                  {showLogs ? 'Hide Logs' : 'Show Logs'}
                </button>
              </div>
            </div>
            
            {queueStatus.is_processing && (
              <div className="processing-indicator">
                <span>⚡ Currently processing files...</span>
              </div>
            )}

            <div className="queue-list">
              {allJobs.map((job) => (
                <div key={job.id} className="queue-item">
                  <div className="job-info">
                    <div className="job-details">
                      <div className="job-name">{job.file_name}</div>
                      <div className="job-meta">
                        {getStatusText(job.status)} • {formatDate(job.created_at)}
                      </div>
                    </div>
                  </div>
                  
                  <div className="job-status">
                    <span className="status-icon">{getStatusIcon(job.status)}</span>
                    
                    {job.status === 'processing' && (
                      <div className="progress-bar">
                        <div 
                          className="progress-fill" 
                          style={{ width: `${job.progress}%` }}
                        />
                        <span className="progress-text">{job.progress}%</span>
                      </div>
                    )}
                    
                    {(job.status === 'queued' || job.status === 'processing') && (
                      <button 
                        className="cancel-job-button"
                        onClick={() => cancelJob(job.id)}
                      >
                        Cancel
                      </button>
                    )}

                    {job.error && (
                      <div className="job-error">
                        Error: {job.error}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Analyzed Files */}
        <section className="analyzed-files-section">
          <h2>Analyzed Files ({analyzedFiles.length})</h2>
          <div className="files-list">
            {analyzedFiles.length === 0 ? (
              <div className="empty-state">
                <p>No files analyzed yet</p>
                <p className="empty-subtext">Upload some footage to get started</p>
              </div>
            ) : (
              analyzedFiles.map((file) => (
                <div key={file.file_name} className="file-item">
                  <div className="file-info">
                    <div className="file-icon">🎥</div>
                    <div className="file-details">
                      <div className="file-name">{file.original_video}</div>
                      <div className="file-meta">
                        {formatFileSize(file.file_size)} • {formatDuration(file.duration_frames, file.fps)} • {file.speakers.length} speaker(s)
                      </div>
                      <div className="file-stats">
                        {file.word_count} words • {file.silence_count} silence periods
                      </div>
                      <div className="file-date">
                        Analyzed: {formatDate(file.analyzed_at)}
                      </div>
                    </div>
                  </div>
                  
                  <div className="file-actions">
                    <button 
                      className="view-transcript-button"
                      onClick={() => viewTranscript(file.file_name)}
                    >
                      View Transcript
                    </button>
                    <button 
                      className="delete-file-button"
                      onClick={() => deleteAnalyzedFile(file.file_name)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </section>
      </div>

      {/* Log Viewer */}
      <LogViewer 
        isVisible={showLogs}
        onToggle={() => setShowLogs(!showLogs)}
        apiUrl="ws://localhost:8001"
      />
    </>
  )
} 