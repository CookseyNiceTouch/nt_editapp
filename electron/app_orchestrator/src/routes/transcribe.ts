import { Router } from 'express';
import { transcribeController } from '../controllers/transcribe';
import { asyncHandler } from '../middleware/errorHandler';
import { validateFileUpload } from '../middleware/validation';

const router = Router();

// POST /api/transcribe
router.post('/', validateFileUpload, asyncHandler(transcribeController));

export default router;
