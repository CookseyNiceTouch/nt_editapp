import { spawn, ChildProcess } from 'child_process';
import path from 'path';
import axios, { AxiosInstance } from 'axios';
import logger from '../utils/logger';
import { config } from '../config';

export interface TranscriptionJob {
  id: string;
  status: string;
  file_name: string;
  progress: number;
  created_at: string;
  updated_at?: string;
  error?: string;
}

export interface QueueStatus {
  queued_jobs: TranscriptionJob[];
  active_jobs: TranscriptionJob[];
  queue_length: number;
  is_processing: boolean;
}

export interface AnalyzedFile {
  file_name: string;
  original_video: string;
  analyzed_at: string;
  file_size: number;
  speakers: string[];
  duration_frames: number;
  fps: number;
  word_count: number;
  silence_count: number;
}

export interface UploadFileRequest {
  file: Buffer;
  fileName: string;
  brief_path?: string;
  custom_spell?: any[];
  silence_threshold_ms?: number;
}

export interface UploadFileResponse {
  job_id: string;
  message: string;
  queue_position: number;
}

class TranscriptionService {
  private apiProcess: ChildProcess | null = null;
  private isReady = false;
  private readonly baseURL: string;
  private readonly apiClient: AxiosInstance;
  private readonly transcriptionBackendPath: string;
  private startupPromise: Promise<void> | null = null;

  constructor() {
    this.baseURL = config.services.transcriptionAPI || 'http://127.0.0.1:8001';
    this.apiClient = axios.create({
      baseURL: this.baseURL,
      timeout: config.security.apiTimeout,
    });
    
    // Path to the transcription backend relative to the app_orchestrator
    // From electron/app_orchestrator, we need to go up two levels to reach the project root, then into backend
    this.transcriptionBackendPath = path.resolve(__dirname, '../../../../backend/transcriptanalysis');
  }

  /**
   * Start the Python transcription API server
   */
  async startAPI(): Promise<void> {
    if (this.startupPromise) {
      return this.startupPromise;
    }

    this.startupPromise = this._startAPIProcess();
    return this.startupPromise;
  }

  private async _startAPIProcess(): Promise<void> {
    if (this.apiProcess || this.isReady) {
      logger.info('Transcription API already running');
      return;
    }

    logger.info('Starting transcription API server...', {
      path: this.transcriptionBackendPath,
      baseURL: this.baseURL
    });

    return new Promise((resolve, reject) => {
      // Use uv run to start the API with proper dependency management
      this.apiProcess = spawn('uv', ['run', 'python', '-m', 'api'], {
        cwd: this.transcriptionBackendPath,
        stdio: ['pipe', 'pipe', 'pipe'],
        env: {
          ...process.env,
          PYTHONPATH: this.transcriptionBackendPath
        }
      });

      // Handle process events
      this.apiProcess.on('error', (error) => {
        logger.error('Transcription API process error:', error);
        this.cleanup();
        reject(new Error(`Failed to start transcription API: ${error.message}`));
      });

      this.apiProcess.on('exit', (code, signal) => {
        logger.warn('Transcription API process exited', { code, signal });
        this.cleanup();
      });

      this.apiProcess.stdout?.on('data', (data) => {
        const output = data.toString();
        logger.debug('Transcription API stdout:', output);
        
        // Look for server startup indication
        if (output.includes('Uvicorn running on') || output.includes('Application startup complete')) {
          this.waitForAPIReady().then(resolve).catch(reject);
        }
      });

      this.apiProcess.stderr?.on('data', (data) => {
        const error = data.toString();
        logger.debug('Transcription API stderr:', error);
        
        // Check for common startup errors
        if (error.includes('Address already in use') || error.includes('Permission denied')) {
          reject(new Error(`Transcription API startup failed: ${error}`));
        }
      });

      // Fallback timeout to check if API is ready
      setTimeout(() => {
        if (!this.isReady) {
          this.waitForAPIReady().then(resolve).catch(reject);
        }
      }, 5000);
    });
  }

  private async waitForAPIReady(maxAttempts: number = 30): Promise<void> {
    for (let i = 0; i < maxAttempts; i++) {
      try {
        const response = await this.apiClient.get('/');
        if (response.status === 200) {
          this.isReady = true;
          logger.info('Transcription API server is ready!', { baseURL: this.baseURL });
          return;
        }
      } catch (error) {
        // API not ready yet, wait and try again
        logger.debug(`API health check attempt ${i + 1}/${maxAttempts} failed`);
      }
      
      await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second
    }
    
    throw new Error(`Transcription API failed to start within ${maxAttempts} seconds`);
  }

  /**
   * Stop the Python transcription API server
   */
  stopAPI(): void {
    if (this.apiProcess) {
      logger.info('Stopping transcription API server...');
      this.apiProcess.kill('SIGTERM');
      
      // Force kill after 5 seconds if it doesn't respond
      setTimeout(() => {
        if (this.apiProcess && !this.apiProcess.killed) {
          logger.warn('Force killing transcription API process');
          this.apiProcess.kill('SIGKILL');
        }
      }, 5000);
    }
    this.cleanup();
  }

  private cleanup(): void {
    this.apiProcess = null;
    this.isReady = false;
    this.startupPromise = null;
  }

  /**
   * Check if the API is healthy and ready
   */
  async checkHealth(): Promise<boolean> {
    if (!this.isReady) return false;
    
    try {
      const response = await this.apiClient.get('/');
      return response.status === 200;
    } catch (error) {
      logger.debug('Health check failed:', error);
      return false;
    }
  }

  /**
   * Get current queue status
   */
  async getQueueStatus(): Promise<QueueStatus> {
    await this.ensureAPIReady();
    
    try {
      const response = await this.apiClient.get('/queue');
      return response.data;
    } catch (error) {
      logger.error('Failed to get queue status:', error);
      throw new Error(`Failed to get queue status: ${this.getErrorMessage(error)}`);
    }
  }

  /**
   * Get specific job status
   */
  async getJobStatus(jobId: string): Promise<TranscriptionJob> {
    await this.ensureAPIReady();
    
    try {
      const response = await this.apiClient.get(`/job/${jobId}`);
      return response.data;
    } catch (error) {
      logger.error('Failed to get job status:', { jobId, error });
      throw new Error(`Failed to get job status: ${this.getErrorMessage(error)}`);
    }
  }

  /**
   * Cancel a specific job
   */
  async cancelJob(jobId: string): Promise<{ message: string }> {
    await this.ensureAPIReady();
    
    try {
      const response = await this.apiClient.delete(`/queue/${jobId}`);
      logger.info('Job cancelled successfully', { jobId });
      return response.data;
    } catch (error) {
      logger.error('Failed to cancel job:', { jobId, error });
      throw new Error(`Failed to cancel job: ${this.getErrorMessage(error)}`);
    }
  }

  /**
   * Clear entire queue
   */
  async clearQueue(): Promise<{ message: string }> {
    await this.ensureAPIReady();
    
    try {
      const response = await this.apiClient.delete('/queue');
      logger.info('Queue cleared successfully');
      return response.data;
    } catch (error) {
      logger.error('Failed to clear queue:', error);
      throw new Error(`Failed to clear queue: ${this.getErrorMessage(error)}`);
    }
  }

  /**
   * Get all analyzed files
   */
  async getAnalyzedFiles(): Promise<AnalyzedFile[]> {
    await this.ensureAPIReady();
    
    try {
      const response = await this.apiClient.get('/analyzed');
      return response.data;
    } catch (error) {
      logger.error('Failed to get analyzed files:', error);
      throw new Error(`Failed to get analyzed files: ${this.getErrorMessage(error)}`);
    }
  }

  /**
   * Get specific analyzed file content
   */
  async getAnalyzedFile(fileName: string): Promise<any> {
    await this.ensureAPIReady();
    
    try {
      const response = await this.apiClient.get(`/analyzed/${fileName}`);
      return response.data;
    } catch (error) {
      logger.error('Failed to get analyzed file:', { fileName, error });
      throw new Error(`Failed to get analyzed file: ${this.getErrorMessage(error)}`);
    }
  }

  /**
   * Delete an analyzed file
   */
  async deleteAnalyzedFile(fileName: string): Promise<{ message: string }> {
    await this.ensureAPIReady();
    
    try {
      const response = await this.apiClient.delete(`/analyzed/${fileName}`);
      logger.info('Analyzed file deleted successfully', { fileName });
      return response.data;
    } catch (error) {
      logger.error('Failed to delete analyzed file:', { fileName, error });
      throw new Error(`Failed to delete analyzed file: ${this.getErrorMessage(error)}`);
    }
  }

  /**
   * Upload a file directly to the API with transcription settings
   */
  async uploadFile(request: UploadFileRequest): Promise<UploadFileResponse> {
    await this.ensureAPIReady();
    
    try {
      const formData = new FormData();
      formData.append('file', new Blob([request.file]), request.fileName);
      
      // Add optional parameters if provided
      if (request.brief_path) {
        formData.append('brief_path', request.brief_path);
      }
      
      if (request.custom_spell) {
        formData.append('custom_spell', JSON.stringify(request.custom_spell));
      }
      
      if (request.silence_threshold_ms !== undefined) {
        formData.append('silence_threshold_ms', request.silence_threshold_ms.toString());
      }
      
      const response = await this.apiClient.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      logger.info('File uploaded successfully', { 
        fileName: request.fileName, 
        job_id: response.data.job_id,
        message: response.data.message 
      });
      return response.data;
    } catch (error) {
      logger.error('Failed to upload file:', { fileName: request.fileName, error });
      throw new Error(`Failed to upload file: ${this.getErrorMessage(error)}`);
    }
  }

  private async ensureAPIReady(): Promise<void> {
    if (!this.isReady) {
      logger.info('API not ready, starting...');
      await this.startAPI();
    }
    
    // Double-check health
    const isHealthy = await this.checkHealth();
    if (!isHealthy) {
      throw new Error('Transcription API is not responding. Please check if the Python backend is properly installed.');
    }
  }

  private getErrorMessage(error: any): string {
    if (axios.isAxiosError(error)) {
      return error.response?.data?.detail || error.message;
    }
    return error instanceof Error ? error.message : String(error);
  }

  /**
   * Get service status info
   */
  getStatus(): { isReady: boolean; baseURL: string; processRunning: boolean } {
    return {
      isReady: this.isReady,
      baseURL: this.baseURL,
      processRunning: this.apiProcess !== null && !this.apiProcess.killed
    };
  }
}

// Export singleton instance
export const transcriptionService = new TranscriptionService();
export default transcriptionService; 