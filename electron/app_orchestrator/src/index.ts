import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';

// Import configuration and utilities
import { config } from './config';
import logger from './utils/logger';

// Import middleware
import { errorHandler, notFoundHandler } from './middleware/errorHandler';

// Import routes
import healthRoutes from './routes/health';
import transcribeRoutes from './routes/transcribe';
import chatbotRoutes from './routes/chatbot';

// Import transcription service for startup/shutdown
import transcriptionService from './services/transcriptionService';

const app = express();

// Security middleware
app.use(helmet());

// CORS configuration
app.use(cors({
  origin: config.security.corsOrigin,
  credentials: true,
}));

// Request parsing middleware
app.use(bodyParser.json({ limit: config.upload.maxFileSize }));
app.use(bodyParser.urlencoded({ extended: true, limit: config.upload.maxFileSize }));

// Request logging
app.use(morgan(config.logging.format));

// Health check routes
app.use('/health', healthRoutes);

// API routes
app.use('/api/transcribe', transcribeRoutes);
app.use('/api/chatbot', chatbotRoutes);

// 404 handler
app.use(notFoundHandler);

// Error handling middleware (must be last)
app.use(errorHandler);

// Graceful shutdown handling
function setupGracefulShutdown() {
  const gracefulShutdown = (signal: string) => {
    logger.info(`🛑 Received ${signal}. Starting graceful shutdown...`);
    
    // Stop transcription service
    transcriptionService.stopAPI();
    
    // Close server
    process.exit(0);
  };

  process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
  process.on('SIGINT', () => gracefulShutdown('SIGINT'));
  
  // Handle uncaught exceptions
  process.on('uncaughtException', (error) => {
    logger.error('Uncaught Exception:', error);
    gracefulShutdown('uncaughtException');
  });
  
  process.on('unhandledRejection', (reason, promise) => {
    logger.error(`Unhandled Rejection at: ${promise}, reason: ${reason}`);
    gracefulShutdown('unhandledRejection');
  });
}

// Start server with transcription service initialization
async function startServer() {
  try {
    // Start the Express server
    const PORT = config.server.port;
    const server = app.listen(PORT, () => {
      logger.info(`🛠  Orchestrator running at http://localhost:${PORT}`);
      logger.info('Available endpoints:');
      logger.info(`  Health: http://localhost:${PORT}/health`);
      logger.info(`  Detailed Health: http://localhost:${PORT}/health/detailed`);
      logger.info(`  Transcribe: http://localhost:${PORT}/api/transcribe`);
      logger.info(`  Transcribe Health: http://localhost:${PORT}/api/transcribe/health`);
      logger.info(`  Chatbot: http://localhost:${PORT}/api/chatbot`);
    });
    
    // Setup graceful shutdown
    setupGracefulShutdown();
    
    // Initialize transcription service in background (don't block startup)
    logger.info('🚀 Initializing transcription service...');
    transcriptionService.startAPI().then(() => {
      logger.info('✅ Transcription service ready');
    }).catch((error) => {
      logger.warn('⚠️  Transcription service failed to start automatically:', error.message);
      logger.info('💡 You can start it manually via POST /api/transcribe/start');
    });
    
  } catch (error) {
    logger.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

// Start the application
startServer(); 