import { Request, Response, NextFunction } from 'express';
import { AppError } from './errorHandler';

export interface ValidationRule {
  field: string;
  required?: boolean;
  type?: 'string' | 'number' | 'boolean' | 'object' | 'array';
  minLength?: number;
  maxLength?: number;
  min?: number;
  max?: number;
  pattern?: RegExp;
  custom?: (value: any) => boolean | string;
}

export const validateRequest = (rules: ValidationRule[], location: 'body' | 'query' | 'params' = 'body') => {
  return (req: Request, res: Response, next: NextFunction): void => {
    const data = req[location];
    const errors: string[] = [];

    for (const rule of rules) {
      const value = data[rule.field];

      // Check required fields
      if (rule.required && (value === undefined || value === null || value === '')) {
        errors.push(`${rule.field} is required`);
        continue;
      }

      // Skip validation if field is not provided and not required
      if (value === undefined || value === null) {
        continue;
      }

      // Type validation
      if (rule.type) {
        const actualType = Array.isArray(value) ? 'array' : typeof value;
        if (actualType !== rule.type) {
          errors.push(`${rule.field} must be of type ${rule.type}`);
          continue;
        }
      }

      // String validations
      if (typeof value === 'string') {
        if (rule.minLength && value.length < rule.minLength) {
          errors.push(`${rule.field} must be at least ${rule.minLength} characters long`);
        }
        if (rule.maxLength && value.length > rule.maxLength) {
          errors.push(`${rule.field} must be at most ${rule.maxLength} characters long`);
        }
        if (rule.pattern && !rule.pattern.test(value)) {
          errors.push(`${rule.field} format is invalid`);
        }
      }

      // Number validations
      if (typeof value === 'number') {
        if (rule.min && value < rule.min) {
          errors.push(`${rule.field} must be at least ${rule.min}`);
        }
        
        if (rule.max && value > rule.max) {
          errors.push(`${rule.field} must be at most ${rule.max}`);
        }
      }

      // Custom validation
      if (rule.custom) {
        const customResult = rule.custom(value);
        if (customResult !== true) {
          errors.push(typeof customResult === 'string' ? customResult : `${rule.field} failed custom validation`);
        }
      }
    }

    if (errors.length > 0) {
      throw new AppError('Validation failed', 400, 'VALIDATION_ERROR', { errors });
    }

    next();
  };
};

// Common validation patterns
export const validateFileUpload = (req: Request, res: Response, next: NextFunction): void => {
  const rules: ValidationRule[] = [
    { field: 'filePath', required: true, type: 'string', minLength: 1 },
  ];
  
  validateRequest(rules, 'body')(req, res, next);
};

export const validatePagination = (req: Request, res: Response, next: NextFunction): void => {
  const rules: ValidationRule[] = [
    { field: 'page', type: 'number', min: 1 },
    { field: 'limit', type: 'number', min: 1, max: 100 },
  ];
  
  validateRequest(rules, 'query')(req, res, next);
}; 