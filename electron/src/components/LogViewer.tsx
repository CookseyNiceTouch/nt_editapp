import { useState, useEffect, useRef } from 'react'

interface LogEntry {
  timestamp: string
  level: string
  logger: string
  message: string
  module?: string
  funcName?: string
  lineno?: number
  job_id?: string
}

interface LogViewerProps {
  isVisible: boolean
  onToggle: () => void
  apiUrl?: string
}

export default function LogViewer({ isVisible, onToggle, apiUrl = 'ws://localhost:8001' }: LogViewerProps) {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const [autoScroll, setAutoScroll] = useState(true)
  const [logLevel, setLogLevel] = useState<string>('ALL')
  const [searchTerm, setSearchTerm] = useState('')
  const [maxLogs, setMaxLogs] = useState(1000)
  
  const wsRef = useRef<WebSocket | null>(null)
  const logsEndRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  // WebSocket connection management
  useEffect(() => {
    if (!isVisible) return

    const connectWebSocket = () => {
      try {
        const ws = new WebSocket(`${apiUrl}/ws/logs`)
        wsRef.current = ws

        ws.onopen = () => {
          setIsConnected(true)
          console.log('Connected to log stream')
        }

        ws.onmessage = (event) => {
          try {
            const logEntry: LogEntry = JSON.parse(event.data)
            setLogs(prevLogs => {
              const newLogs = [...prevLogs, logEntry]
              // Keep only the latest maxLogs entries
              if (newLogs.length > maxLogs) {
                return newLogs.slice(-maxLogs)
              }
              return newLogs
            })
          } catch (error) {
            console.error('Error parsing log message:', error)
          }
        }

        ws.onclose = () => {
          setIsConnected(false)
          console.log('Disconnected from log stream')
          // Attempt to reconnect after 3 seconds
          setTimeout(connectWebSocket, 3000)
        }

        ws.onerror = (error) => {
          console.error('WebSocket error:', error)
          setIsConnected(false)
        }

        // Send periodic ping to keep connection alive
        const pingInterval = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send('ping')
          }
        }, 25000)

        return () => {
          clearInterval(pingInterval)
          ws.close()
        }
      } catch (error) {
        console.error('Error connecting to WebSocket:', error)
      }
    }

    const cleanup = connectWebSocket()
    return cleanup
  }, [isVisible, apiUrl, maxLogs])

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (autoScroll && logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [logs, autoScroll])

  // Handle manual scroll detection
  const handleScroll = () => {
    if (!containerRef.current) return
    
    const { scrollTop, scrollHeight, clientHeight } = containerRef.current
    const isAtBottom = scrollTop + clientHeight >= scrollHeight - 10
    
    if (isAtBottom !== autoScroll) {
      setAutoScroll(isAtBottom)
    }
  }

  const clearLogs = () => {
    setLogs([])
  }

  const exportLogs = () => {
    const filteredLogs = getFilteredLogs()
    const logText = filteredLogs.map(log => 
      `${log.timestamp} [${log.level}] ${log.logger}: ${log.message}`
    ).join('\n')
    
    const blob = new Blob([logText], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `transcription-logs-${new Date().toISOString().slice(0, 19)}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const getFilteredLogs = () => {
    return logs.filter(log => {
      const levelMatch = logLevel === 'ALL' || log.level === logLevel
      const searchMatch = searchTerm === '' || 
        log.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.logger.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (log.job_id && log.job_id.toLowerCase().includes(searchTerm.toLowerCase()))
      
      return levelMatch && searchMatch
    })
  }

  const formatTimestamp = (timestamp: string) => {
    try {
      return new Date(timestamp).toLocaleTimeString()
    } catch {
      return timestamp
    }
  }

  const getLogLevelColor = (level: string) => {
    switch (level) {
      case 'ERROR': return '#ff6b6b'
      case 'WARNING': return '#ffa726'
      case 'INFO': return '#61dafb'
      case 'DEBUG': return '#cccccc'
      default: return '#ffffff'
    }
  }

  const getLogLevelIcon = (level: string) => {
    switch (level) {
      case 'ERROR': return '❌'
      case 'WARNING': return '⚠️'
      case 'INFO': return 'ℹ️'
      case 'DEBUG': return '🔍'
      default: return '📝'
    }
  }

  const filteredLogs = getFilteredLogs()

  if (!isVisible) {
    return (
      <div className="log-viewer-collapsed">
        <button className="log-toggle-button" onClick={onToggle}>
          <span className="log-icon">📋</span>
          Show Logs
          {isConnected && <span className="connection-indicator connected">●</span>}
        </button>
      </div>
    )
  }

  return (
    <div className="log-viewer-expanded">
      {/* Header */}
      <div className="log-header">
        <div className="log-header-left">
          <button className="log-toggle-button" onClick={onToggle}>
            <span className="log-icon">📋</span>
            Hide Logs
          </button>
          <div className="connection-status">
            <span className={`connection-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
              ●
            </span>
            <span className="connection-text">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          <div className="log-count">
            {filteredLogs.length} / {logs.length} logs
          </div>
        </div>
        
        <div className="log-header-right">
          <button className="log-action-button" onClick={clearLogs}>
            Clear
          </button>
          <button className="log-action-button" onClick={exportLogs}>
            Export
          </button>
        </div>
      </div>

      {/* Controls */}
      <div className="log-controls">
        <div className="log-control-group">
          <label>Level:</label>
          <select 
            value={logLevel} 
            onChange={(e) => setLogLevel(e.target.value)}
            className="log-select"
          >
            <option value="ALL">All</option>
            <option value="DEBUG">Debug</option>
            <option value="INFO">Info</option>
            <option value="WARNING">Warning</option>
            <option value="ERROR">Error</option>
          </select>
        </div>
        
        <div className="log-control-group">
          <label>Search:</label>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search logs..."
            className="log-search-input"
          />
        </div>
        
        <div className="log-control-group">
          <label className="auto-scroll-label">
            <input
              type="checkbox"
              checked={autoScroll}
              onChange={(e) => setAutoScroll(e.target.checked)}
            />
            Auto-scroll
          </label>
        </div>
      </div>

      {/* Log Display */}
      <div 
        className="log-container"
        ref={containerRef}
        onScroll={handleScroll}
      >
        {filteredLogs.length === 0 ? (
          <div className="log-empty">
            {logs.length === 0 ? 'No logs yet...' : 'No logs match current filters'}
          </div>
        ) : (
          filteredLogs.map((log, index) => (
            <div 
              key={index} 
              className={`log-entry log-level-${log.level.toLowerCase()}`}
            >
              <div className="log-entry-header">
                <span className="log-timestamp">
                  {formatTimestamp(log.timestamp)}
                </span>
                <span 
                  className="log-level"
                  style={{ color: getLogLevelColor(log.level) }}
                >
                  {getLogLevelIcon(log.level)} {log.level}
                </span>
                <span className="log-logger">{log.logger}</span>
                {log.job_id && (
                  <span className="log-job-id">#{log.job_id.slice(0, 8)}</span>
                )}
              </div>
              <div className="log-message">{log.message}</div>
              {(log.module || log.funcName) && (
                <div className="log-location">
                  {log.module}:{log.funcName}:{log.lineno}
                </div>
              )}
            </div>
          ))
        )}
        <div ref={logsEndRef} />
      </div>
    </div>
  )
} 