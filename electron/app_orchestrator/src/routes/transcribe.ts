import { Router, Request } from 'express';
import { 
  uploadFile,
  getQueueStatus,
  getJobStatus,
  cancelJob,
  clearQueue,
  getAnalyzedFiles,
  getAnalyzedFile,
  deleteAnalyzedFile,
  getServiceHealth,
  startService,
  stopService,
  transcribeController
} from '../controllers/transcribe';
import { asyncHandler } from '../middleware/errorHandler';
import multer from 'multer';

const router = Router();

// Configure multer for file uploads
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 500 * 1024 * 1024, // 500MB limit
  },
  fileFilter: (req: Request, file: Express.Multer.File, cb: multer.FileFilterCallback) => {
    const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/wmv', 'video/x-msvideo'];
    if (allowedTypes.includes(file.mimetype) || file.originalname.match(/\.(mp4|avi|mov|mkv|wmv|flv|webm)$/i)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only video files are allowed.'));
    }
  }
});

// Service Management Routes
router.get('/health', asyncHandler(getServiceHealth));
router.post('/start', asyncHandler(startService));
router.post('/stop', asyncHandler(stopService));

// Queue Management Routes - Only upload is supported now
router.post('/upload', upload.single('file'), asyncHandler(uploadFile));
router.get('/queue', asyncHandler(getQueueStatus));
router.get('/queue/:jobId', asyncHandler(getJobStatus));
router.delete('/queue/:jobId', asyncHandler(cancelJob));
router.delete('/queue', asyncHandler(clearQueue));

// Analyzed Files Management Routes
router.get('/analyzed', asyncHandler(getAnalyzedFiles));
router.get('/analyzed/:fileName', asyncHandler(getAnalyzedFile));
router.delete('/analyzed/:fileName', asyncHandler(deleteAnalyzedFile));

// Legacy route for backward compatibility - now uses upload
router.post('/', upload.single('file'), asyncHandler(transcribeController));

export default router;
