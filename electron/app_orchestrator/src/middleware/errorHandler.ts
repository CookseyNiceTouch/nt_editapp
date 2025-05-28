import { Request, Response, NextFunction } from 'express';
import { config } from '../config';

export interface ApiError extends Error {
  statusCode?: number;
  code?: string;
  details?: any;
}

export class AppError extends Error implements ApiError {
  public statusCode: number;
  public code: string;
  public details?: any;

  constructor(message: string, statusCode: number = 500, code: string = 'INTERNAL_ERROR', details?: any) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
    this.name = 'AppError';

    Error.captureStackTrace(this, this.constructor);
  }
}

export const errorHandler = (
  err: ApiError,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const statusCode = err.statusCode || 500;
  const isDevelopment = config.server.nodeEnv === 'development';

  // Log error details
  console.error('🚨 Error occurred:', {
    message: err.message,
    statusCode,
    code: err.code,
    stack: isDevelopment ? err.stack : undefined,
    url: req.url,
    method: req.method,
    body: req.body,
    query: req.query,
    timestamp: new Date().toISOString(),
  });

  // Prepare error response
  const errorResponse: any = {
    success: false,
    error: {
      message: err.message,
      code: err.code || 'INTERNAL_ERROR',
      statusCode,
    },
  };

  // Add additional details in development
  if (isDevelopment) {
    errorResponse.error.stack = err.stack;
    errorResponse.error.details = err.details;
  }

  // Send error response
  res.status(statusCode).json(errorResponse);
};

export const asyncHandler = (fn: Function) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

export const notFoundHandler = (req: Request, res: Response, next: NextFunction): void => {
  const error = new AppError(`Route ${req.method} ${req.originalUrl} not found`, 404, 'ROUTE_NOT_FOUND');
  next(error);
}; 