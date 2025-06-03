import dotenv from 'dotenv';

dotenv.config();

interface Config {
  server: {
    port: number;
    nodeEnv: string;
  };
  services: {
    chatbot: string;
    transcribe: string;
    transcriptionAPI: string;
  };
  security: {
    corsOrigin: string;
    apiTimeout: number;
  };
  logging: {
    level: string;
    format: string;
  };
  upload: {
    maxFileSize: string;
    timeout: number;
  };
}

function getEnvVar(key: string, defaultValue?: string): string {
  const value = process.env[key] || defaultValue;
  if (!value) {
    throw new Error(`Environment variable ${key} is required`);
  }
  return value;
}

function getEnvVarAsNumber(key: string, defaultValue?: number): number {
  const value = process.env[key];
  if (!value) {
    if (defaultValue !== undefined) return defaultValue;
    throw new Error(`Environment variable ${key} is required`);
  }
  const parsed = parseInt(value, 10);
  if (isNaN(parsed)) {
    throw new Error(`Environment variable ${key} must be a valid number`);
  }
  return parsed;
}

export const config: Config = {
  server: {
    port: getEnvVarAsNumber('BACKEND_PORT', 4000),
    nodeEnv: getEnvVar('NODE_ENV', 'development'),
  },
  services: {
    chatbot: getEnvVar('CHATBOT_SERVICE_URL', 'http://localhost:5001'),
    transcribe: getEnvVar('TRANSCRIBE_SERVICE_URL', 'http://localhost:5002'),
    transcriptionAPI: getEnvVar('TRANSCRIPTION_API_URL', 'http://127.0.0.1:8000'),
  },
  security: {
    corsOrigin: getEnvVar('CORS_ORIGIN', 'http://localhost:5173'),
    apiTimeout: getEnvVarAsNumber('API_TIMEOUT', 30000),
  },
  logging: {
    level: getEnvVar('LOG_LEVEL', 'info'),
    format: getEnvVar('LOG_FORMAT', 'combined'),
  },
  upload: {
    maxFileSize: getEnvVar('MAX_FILE_SIZE', '50mb'),
    timeout: getEnvVarAsNumber('UPLOAD_TIMEOUT', 60000),
  },
};

export default config; 