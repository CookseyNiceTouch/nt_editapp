import { useState } from 'react'

interface AnalyzedFile {
  id: string
  name: string
  size: number
  type: string
  status: 'pending' | 'processing' | 'completed' | 'error'
  progress?: number
  transcript?: string
  duration?: string
}

interface FootageIngestProps {
  // No props needed for now, but we can add them later if needed
}

export default function FootageIngest({}: FootageIngestProps) {
  const [isDragOver, setIsDragOver] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [isPaused, setIsPaused] = useState(false)
  const [analyzedFiles] = useState<AnalyzedFile[]>([
    // Mock data for UI demonstration
    {
      id: '1',
      name: 'interview_footage.mp4',
      size: 245760000, // ~245MB
      type: 'video/mp4',
      status: 'completed',
      progress: 100,
      transcript: 'This is a sample transcript...',
      duration: '15:32'
    },
    {
      id: '2',
      name: 'background_music.mp3',
      size: 8960000, // ~8.9MB
      type: 'audio/mp3',
      status: 'processing',
      progress: 65,
      duration: '3:45'
    },
    {
      id: '3',
      name: 'outro_clip.mov',
      size: 134217728, // ~134MB
      type: 'video/quicktime',
      status: 'pending',
      duration: '0:45'
    }
  ])

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
    
    const files = Array.from(e.dataTransfer.files)
    console.log('Dropped files:', files)
    // TODO: Handle dropped files
  }

  // Handle file input
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    console.log('Selected files:', files)
    // TODO: Handle selected files
  }

  const openImportDialog = () => {
    // TODO: Open file import dialog
    console.log('Opening import dialog...')
  }

  const handleCancel = () => {
    setIsProcessing(false)
    setIsPaused(false)
    console.log('Cancelling transcription...')
  }

  const handlePauseResume = () => {
    setIsPaused(!isPaused)
    console.log(isPaused ? 'Resuming...' : 'Pausing...')
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getStatusIcon = (status: AnalyzedFile['status']) => {
    switch (status) {
      case 'completed': return '✅'
      case 'processing': return '⏳'
      case 'pending': return '⏸️'
      case 'error': return '❌'
      default: return '📄'
    }
  }

  const getStatusText = (status: AnalyzedFile['status']) => {
    switch (status) {
      case 'completed': return 'Completed'
      case 'processing': return 'Processing...'
      case 'pending': return 'Pending'
      case 'error': return 'Error'
      default: return 'Unknown'
    }
  }

  return (
    <div className="footage-panel">
      {/* File Drop Zone */}
      <section className="file-upload-section">
        <h2>Import Footage</h2>
        <div 
          className={`drop-zone ${isDragOver ? 'drag-over' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="drop-zone-content">
            <div className="drop-icon">📁</div>
            <p className="drop-text">
              Drag and drop your video/audio files here
            </p>
            <p className="drop-subtext">
              or
            </p>
            <button className="import-button" onClick={openImportDialog}>
              Browse Files
            </button>
            <input
              type="file"
              multiple
              accept="video/*,audio/*"
              onChange={handleFileSelect}
              className="hidden-file-input"
              id="file-input"
            />
          </div>
        </div>
      </section>

      {/* Transcription Controls */}
      <section className="transcription-controls">
        <h2>Analysis Controls</h2>
        <div className="control-buttons">
          <button 
            className="control-button cancel-button"
            onClick={handleCancel}
            disabled={!isProcessing}
          >
            Cancel Analysis
          </button>
          <button 
            className="control-button pause-button"
            onClick={handlePauseResume}
            disabled={!isProcessing}
          >
            {isPaused ? '▶️ Resume' : '⏸️ Pause'} Analysis
          </button>
        </div>
        {isProcessing && (
          <div className="processing-status">
            <span className="status-indicator">
              {isPaused ? '⏸️ Paused' : '⏳ Processing...'}
            </span>
          </div>
        )}
      </section>

      {/* File List */}
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
              <div key={file.id} className="file-item">
                <div className="file-info">
                  <div className="file-icon">
                    {file.type.startsWith('video/') ? '🎥' : '🎵'}
                  </div>
                  <div className="file-details">
                    <div className="file-name">{file.name}</div>
                    <div className="file-meta">
                      {formatFileSize(file.size)} • {file.duration}
                    </div>
                  </div>
                </div>
                
                <div className="file-status">
                  <div className="status-info">
                    <span className="status-icon">{getStatusIcon(file.status)}</span>
                    <span className="status-text">{getStatusText(file.status)}</span>
                  </div>
                  
                  {file.status === 'processing' && file.progress && (
                    <div className="progress-bar">
                      <div 
                        className="progress-fill" 
                        style={{ width: `${file.progress}%` }}
                      />
                      <span className="progress-text">{file.progress}%</span>
                    </div>
                  )}
                  
                  {file.status === 'completed' && (
                    <button className="view-transcript-button">
                      View Transcript
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  )
} 