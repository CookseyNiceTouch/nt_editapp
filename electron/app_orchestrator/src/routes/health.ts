import { Router } from 'express';
import { Request, Response } from 'express';
import { asyncHandler } from '../middleware/errorHandler';
import { checkServiceHealth } from '../services/pythonService';
import { config } from '../config';

const router = Router();

// GET /health - Basic health check
router.get('/', (req: Request, res: Response) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    environment: config.server.nodeEnv,
  });
});

// GET /health/detailed - Detailed health check with service status
router.get('/detailed', asyncHandler(async (req: Request, res: Response) => {
  const serviceHealth = await checkServiceHealth();
  
  const allServicesHealthy = Object.values(serviceHealth).every(healthy => healthy);
  
  res.json({
    status: allServicesHealthy ? 'ok' : 'degraded',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    environment: config.server.nodeEnv,
    services: {
      chatbot: {
        url: config.services.chatbot,
        healthy: serviceHealth['chatbot'] || false,
      },
      transcribe: {
        url: config.services.transcribe,
        healthy: serviceHealth['transcribe'] || false,
      },
    },
    configuration: {
      port: config.server.port,
      corsOrigin: config.security.corsOrigin,
      apiTimeout: config.security.apiTimeout,
      maxFileSize: config.upload.maxFileSize,
    }
  });
}));

export default router; 