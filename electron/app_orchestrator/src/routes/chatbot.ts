import { Router } from 'express';
import { chatbotController } from '../controllers/chatbot';
import { asyncHandler } from '../middleware/errorHandler';
import { validateRequest } from '../middleware/validation';

const router = Router();

// POST /api/chatbot
router.post('/', 
  validateRequest([
    { field: 'message', required: true, type: 'string', minLength: 1 }
  ]), 
  asyncHandler(chatbotController)
);

export default router;
