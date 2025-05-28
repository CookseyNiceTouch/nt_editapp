import { Request, Response } from 'express';
import { AppError } from '../middleware/errorHandler';
import logger from '../utils/logger';

export async function transcribeController(req: Request, res: Response): Promise<void> {
  const { filePath } = req.body;
  
  logger.info('Transcription request received', { filePath });

  try {
    // TODO: Implement transcription service call
    // This will call the Python transcription service
    
    logger.info('Transcription completed successfully', { filePath });
    
    res.json({ 
      success: true, 
      transcript: null, // Placeholder - will contain actual transcript
      message: 'Transcription service not yet implemented'
    });
  } catch (error) {
    logger.error('Transcription failed', { filePath, error: (error as Error).message });
    throw new AppError('Transcription service failed', 500, 'TRANSCRIPTION_ERROR');
  }
}
