import { config } from '../config';

export type LogLevel = 'error' | 'warn' | 'info' | 'debug';

interface LogEntry {
  level: LogLevel;
  message: string;
  timestamp: string;
  data?: any;
}

class Logger {
  private logLevel: LogLevel;

  constructor() {
    this.logLevel = (config.logging.level as LogLevel) || 'info';
  }

  private shouldLog(level: LogLevel): boolean {
    const levels: LogLevel[] = ['error', 'warn', 'info', 'debug'];
    const currentLevelIndex = levels.indexOf(this.logLevel);
    const requestedLevelIndex = levels.indexOf(level);
    
    return requestedLevelIndex <= currentLevelIndex;
  }

  private formatMessage(entry: LogEntry): string {
    const { level, message, timestamp, data } = entry;
    const prefix = `[${timestamp}] [${level.toUpperCase()}]`;
    
    if (data) {
      return `${prefix} ${message}\n${JSON.stringify(data, null, 2)}`;
    }
    
    return `${prefix} ${message}`;
  }

  private createLogEntry(level: LogLevel, message: string, data?: any): LogEntry {
    return {
      level,
      message,
      timestamp: new Date().toISOString(),
      data,
    };
  }

  private writeLog(entry: LogEntry): void {
    if (!this.shouldLog(entry.level)) {
      return;
    }

    const formattedMessage = this.formatMessage(entry);
    
    switch (entry.level) {
      case 'error':
        console.error(formattedMessage);
        break;
      case 'warn':
        console.warn(formattedMessage);
        break;
      case 'info':
        console.info(formattedMessage);
        break;
      case 'debug':
        console.debug(formattedMessage);
        break;
    }
  }

  error(message: string, data?: any): void {
    this.writeLog(this.createLogEntry('error', message, data));
  }

  warn(message: string, data?: any): void {
    this.writeLog(this.createLogEntry('warn', message, data));
  }

  info(message: string, data?: any): void {
    this.writeLog(this.createLogEntry('info', message, data));
  }

  debug(message: string, data?: any): void {
    this.writeLog(this.createLogEntry('debug', message, data));
  }

  // HTTP request logging
  request(method: string, url: string, statusCode?: number, duration?: number): void {
    const message = `${method} ${url}`;
    const data = { statusCode, duration: duration ? `${duration}ms` : undefined };
    this.info(message, data);
  }

  // Service communication logging
  service(serviceName: string, action: string, data?: any): void {
    const message = `Service: ${serviceName} - ${action}`;
    this.debug(message, data);
  }
}

export const logger = new Logger();
export default logger;
