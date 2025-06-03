import { Request, Response } from 'express';
import { AppError } from '../middleware/errorHandler';
import logger from '../utils/logger';
import transcriptionService, { UploadFileRequest } from '../services/transcriptionService';

// Types for request/response validation
interface UploadFileBody {
  brief_path?: string;
  custom_spell?: any[];
  silence_threshold_ms?: number;
}

/**
 * Upload a file and add it to the transcription queue
 */
export async function uploadFile(req: Request, res: Response): Promise<void> {
  logger.info('File upload and queue request received');

  try {
    // Type assertion for multer file
    const file = (req as any).file as Express.Multer.File;
    const body = req.body as UploadFileBody;
    
    if (!file) {
      throw new AppError('No file provided', 400, 'MISSING_FILE');
    }

    // Parse custom_spell if it's a string (from form data)
    let parsedCustomSpell: any[] | undefined;
    if (body.custom_spell) {
      try {
        parsedCustomSpell = typeof body.custom_spell === 'string' 
          ? JSON.parse(body.custom_spell) 
          : body.custom_spell;
      } catch (error) {
        logger.warn('Invalid custom_spell JSON, ignoring', { custom_spell: body.custom_spell });
      }
    }

    const uploadRequest: UploadFileRequest = {
      file: file.buffer,
      fileName: file.originalname,
      ...(body.brief_path && { brief_path: body.brief_path }),
      ...(parsedCustomSpell && { custom_spell: parsedCustomSpell }),
      ...(body.silence_threshold_ms !== undefined && { silence_threshold_ms: body.silence_threshold_ms })
    };

    const result = await transcriptionService.uploadFile(uploadRequest);
    
    logger.info('File uploaded and queued successfully', { 
      file_name: file.originalname,
      job_id: result.job_id,
      queue_position: result.queue_position,
      message: result.message
    });
    
    res.json({ 
      success: true, 
      job_id: result.job_id,
      message: result.message,
      queue_position: result.queue_position,
      file_name: file.originalname
    });
  } catch (error) {
    logger.error('Failed to upload and queue file', { error: (error as Error).message });
    throw new AppError('Failed to upload and queue file', 500, 'FILE_UPLOAD_ERROR');
  }
}

/**
 * Get current transcription queue status
 */
export async function getQueueStatus(req: Request, res: Response): Promise<void> {
  logger.info('Queue status request received');

  try {
    const status = await transcriptionService.getQueueStatus();
    
    logger.debug('Queue status retrieved', { 
      queue_length: status.queue_length,
      is_processing: status.is_processing 
    });
    
    res.json({ 
      success: true, 
      ...status 
    });
  } catch (error) {
    logger.error('Failed to get queue status', { error: (error as Error).message });
    throw new AppError('Failed to get queue status', 500, 'QUEUE_STATUS_ERROR');
  }
}

/**
 * Get specific job status
 */
export async function getJobStatus(req: Request, res: Response): Promise<void> {
  const { jobId } = req.params;
  
  logger.info('Job status request', { jobId });

  try {
    if (!jobId) {
      throw new AppError('Job ID is required', 400, 'MISSING_JOB_ID');
    }

    const status = await transcriptionService.getJobStatus(jobId);
    
    logger.debug('Job status retrieved', { jobId, status: status.status, progress: status.progress });
    
    res.json({ 
      success: true, 
      job: status 
    });
  } catch (error) {
    logger.error('Failed to get job status', { jobId, error: (error as Error).message });
    throw new AppError('Failed to get job status', 500, 'JOB_STATUS_ERROR');
  }
}

/**
 * Cancel a specific transcription job
 */
export async function cancelJob(req: Request, res: Response): Promise<void> {
  const { jobId } = req.params;
  
  logger.info('Cancel job request', { jobId });

  try {
    if (!jobId) {
      throw new AppError('Job ID is required', 400, 'MISSING_JOB_ID');
    }

    const result = await transcriptionService.cancelJob(jobId);
    
    logger.info('Job cancelled successfully', { jobId });
    
    res.json({ 
      success: true, 
      message: result.message 
    });
  } catch (error) {
    logger.error('Failed to cancel job', { jobId, error: (error as Error).message });
    throw new AppError('Failed to cancel job', 500, 'JOB_CANCEL_ERROR');
  }
}

/**
 * Clear the entire transcription queue
 */
export async function clearQueue(req: Request, res: Response): Promise<void> {
  logger.info('Clear queue request received');

  try {
    const result = await transcriptionService.clearQueue();
    
    logger.info('Queue cleared successfully');
    
    res.json({ 
      success: true, 
      message: result.message 
    });
  } catch (error) {
    logger.error('Failed to clear queue', { error: (error as Error).message });
    throw new AppError('Failed to clear queue', 500, 'QUEUE_CLEAR_ERROR');
  }
}

/**
 * Get all analyzed transcription files
 */
export async function getAnalyzedFiles(req: Request, res: Response): Promise<void> {
  logger.info('Get analyzed files request received');

  try {
    const files = await transcriptionService.getAnalyzedFiles();
    
    logger.debug('Analyzed files retrieved', { count: files.length });
    
    res.json({ 
      success: true, 
      files 
    });
  } catch (error) {
    logger.error('Failed to get analyzed files', { error: (error as Error).message });
    throw new AppError('Failed to get analyzed files', 500, 'ANALYZED_FILES_ERROR');
  }
}

/**
 * Get specific analyzed file content
 */
export async function getAnalyzedFile(req: Request, res: Response): Promise<void> {
  const { fileName } = req.params;
  
  logger.info('Get analyzed file request', { fileName });

  try {
    if (!fileName) {
      throw new AppError('File name is required', 400, 'MISSING_FILE_NAME');
    }

    const fileContent = await transcriptionService.getAnalyzedFile(fileName);
    
    logger.debug('Analyzed file content retrieved', { fileName });
    
    res.json({ 
      success: true, 
      file: fileContent 
    });
  } catch (error) {
    logger.error('Failed to get analyzed file', { fileName, error: (error as Error).message });
    throw new AppError('Failed to get analyzed file', 500, 'ANALYZED_FILE_ERROR');
  }
}

/**
 * Delete an analyzed file
 */
export async function deleteAnalyzedFile(req: Request, res: Response): Promise<void> {
  const { fileName } = req.params;
  
  logger.info('Delete analyzed file request', { fileName });

  try {
    if (!fileName) {
      throw new AppError('File name is required', 400, 'MISSING_FILE_NAME');
    }

    const result = await transcriptionService.deleteAnalyzedFile(fileName);
    
    logger.info('Analyzed file deleted successfully', { fileName });
    
    res.json({ 
      success: true, 
      message: result.message 
    });
  } catch (error) {
    logger.error('Failed to delete analyzed file', { fileName, error: (error as Error).message });
    throw new AppError('Failed to delete analyzed file', 500, 'DELETE_FILE_ERROR');
  }
}

/**
 * Get transcription service health status
 */
export async function getServiceHealth(req: Request, res: Response): Promise<void> {
  logger.info('Service health check request received');

  try {
    const isHealthy = await transcriptionService.checkHealth();
    const status = transcriptionService.getStatus();
    
    res.json({ 
      success: true, 
      healthy: isHealthy,
      ...status
    });
  } catch (error) {
    logger.error('Failed to check service health', { error: (error as Error).message });
    throw new AppError('Failed to check service health', 500, 'HEALTH_CHECK_ERROR');
  }
}

/**
 * Start the transcription API service
 */
export async function startService(req: Request, res: Response): Promise<void> {
  logger.info('Start transcription service request received');

  try {
    await transcriptionService.startAPI();
    
    logger.info('Transcription service started successfully');
    
    res.json({ 
      success: true, 
      message: 'Transcription service started successfully' 
    });
  } catch (error) {
    logger.error('Failed to start transcription service', { error: (error as Error).message });
    throw new AppError('Failed to start transcription service', 500, 'SERVICE_START_ERROR');
  }
}

/**
 * Stop the transcription API service
 */
export async function stopService(req: Request, res: Response): Promise<void> {
  logger.info('Stop transcription service request received');

  try {
    transcriptionService.stopAPI();
    
    logger.info('Transcription service stopped successfully');
    
    res.json({ 
      success: true, 
      message: 'Transcription service stopped successfully' 
    });
  } catch (error) {
    logger.error('Failed to stop transcription service', { error: (error as Error).message });
    throw new AppError('Failed to stop transcription service', 500, 'SERVICE_STOP_ERROR');
  }
}

// Legacy controller for backward compatibility
export async function transcribeController(req: Request, res: Response): Promise<void> {
  logger.warn('Legacy transcribeController called - redirecting to addFileToQueue');
  await uploadFile(req, res);
}
