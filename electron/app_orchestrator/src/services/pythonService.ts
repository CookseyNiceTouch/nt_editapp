import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { config } from '../config';
import logger from '../utils/logger';
import { AppError } from '../middleware/errorHandler';

interface ServiceResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

class PythonServiceClient {
  private client: AxiosInstance;

  constructor(baseURL: string, serviceName: string) {
    this.client = axios.create({
      baseURL,
      timeout: config.security.apiTimeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for logging
    this.client.interceptors.request.use(
      (config) => {
        logger.service(serviceName, `${config.method?.toUpperCase()} ${config.url}`, {
          data: config.data,
        });
        return config;
      },
      (error) => {
        logger.error(`Service ${serviceName} request failed`, { error: error.message });
        return Promise.reject(error);
      }
    );

    // Response interceptor for logging
    this.client.interceptors.response.use(
      (response) => {
        logger.service(serviceName, 'Response received', {
          status: response.status,
          data: response.data,
        });
        return response;
      },
      (error) => {
        const errorMessage = error.response?.data?.message || error.message;
        logger.error(`Service ${serviceName} response failed`, {
          status: error.response?.status,
          message: errorMessage,
        });
        return Promise.reject(error);
      }
    );
  }

  async post<T = any>(endpoint: string, data: any): Promise<ServiceResponse<T>> {
    try {
      const response: AxiosResponse<T> = await this.client.post(endpoint, data);
      return {
        success: true,
        data: response.data,
      };
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || error.message;
      return {
        success: false,
        error: errorMessage,
      };
    }
  }

  async get<T = any>(endpoint: string, params?: any): Promise<ServiceResponse<T>> {
    try {
      const response: AxiosResponse<T> = await this.client.get(endpoint, { params });
      return {
        success: true,
        data: response.data,
      };
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || error.message;
      return {
        success: false,
        error: errorMessage,
      };
    }
  }
}

// Service instances
export const chatbotService = new PythonServiceClient(config.services.chatbot, 'chatbot');
export const transcribeService = new PythonServiceClient(config.services.transcribe, 'transcribe');

// Health check for all services
export async function checkServiceHealth(): Promise<{ [key: string]: boolean }> {
  const services = {
    chatbot: chatbotService,
    transcribe: transcribeService,
  };

  const healthChecks = await Promise.allSettled(
    Object.entries(services).map(async ([name, service]) => {
      try {
        const response = await service.get('/health');
        return { name, healthy: response.success };
      } catch (error) {
        return { name, healthy: false };
      }
    })
  );

  const healthStatus: { [key: string]: boolean } = {};
  healthChecks.forEach((result) => {
    if (result.status === 'fulfilled') {
      healthStatus[result.value.name] = result.value.healthy;
    } else {
      healthStatus['unknown'] = false;
    }
  });

  return healthStatus;
} 