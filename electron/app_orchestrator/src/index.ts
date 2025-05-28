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

// Start server
const PORT = config.server.port;
app.listen(PORT, () => {
  logger.info(`🛠  Orchestrator running at http://localhost:${PORT}`);
  logger.info('Available endpoints:', {
    health: `http://localhost:${PORT}/health`,
    detailedHealth: `http://localhost:${PORT}/health/detailed`,
    transcribe: `http://localhost:${PORT}/api/transcribe`,
    chatbot: `http://localhost:${PORT}/api/chatbot`,
  });
}); 