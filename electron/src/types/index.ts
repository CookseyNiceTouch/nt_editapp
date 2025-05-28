// Common types for the application

export interface Message {
  text: string
  sender: 'user' | 'bot'
  timestamp?: Date
}

export interface FileInfo {
  name: string
  size: number
  type: string
}

export interface AnalyzedFile {
  id: string
  name: string
  size: number
  type: string
  status: 'pending' | 'processing' | 'completed' | 'error'
  progress?: number
  transcript?: string
  duration?: string
}

export interface TranscriptionResult {
  transcript: string
  confidence?: number
  language?: string
}

export interface ChatResponse {
  response: string
  success: boolean
  message?: string
}

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

export type TabType = 'footage' | 'chatbot' 