# App Orchestrator

A streamlined Node.js/Express orchestrator service that bridges the Electron frontend with Python backend services for chatbot interactions and audio transcription.

## 🏗️ Architecture

```
Electron Frontend ↔ Node.js Orchestrator ↔ Python Services
                       (This Service)      (chatbot, transcribe)
```

**Core Responsibilities:**
- **Chatbot Communication**: Direct interface to AI chatbot service
- **Audio Transcription**: Handle audio file transcription requests
- **Service Coordination**: Health monitoring and request routing

*Note: Edit generation and automation tasks are handled directly through the chatbot service.*

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation
```bash
npm install
```

### Configuration
Copy the environment template and configure:
```bash
cp env.example .env
```

Edit `.env` with your settings:
```env
BACKEND_PORT=4000
NODE_ENV=development
CHATBOT_SERVICE_URL=http://localhost:5001
TRANSCRIBE_SERVICE_URL=http://localhost:5002
```

### Development
```bash
npm run dev
```

### Production
```bash
npm run build
npm start
```

## 📡 API Endpoints

### Health Checks
- `GET /health` - Basic health status
- `GET /health/detailed` - Detailed health with service status

### Core Services
- `POST /api/chatbot` - Chat with AI assistant
  - Handles: Direct chat, edit generation requests, automation tasks
- `POST /api/transcribe` - Transcribe audio files
  - Handles: Audio file processing and text extraction

## 🔧 Service Communication

Each Python service should expose:
- `GET /health` - Health check endpoint
- Service-specific endpoints for functionality

### Expected Python Services:
1. **Chatbot Service** (Port 5001)
   - Handles AI conversations
   - Processes edit generation requests
   - Manages automation workflows
   
2. **Transcription Service** (Port 5002)
   - Processes audio files
   - Returns transcribed text
   - Supports multiple audio formats

## 📁 Project Structure

```
src/
├── config/          # Environment configuration
├── controllers/     # Request handlers (chatbot, transcribe)
├── middleware/      # Express middleware
├── routes/          # API route definitions
├── services/        # External service clients
├── utils/           # Utility functions
└── index.ts         # Main server entry point
```

## 🛡️ Security

- Helmet for security headers
- CORS configuration
- Request validation
- Error handling with sanitized responses

## 📊 Logging

Structured logging with different levels:
- `error` - Error conditions
- `warn` - Warning conditions  
- `info` - General information
- `debug` - Debug information

## 🧪 Development

### Scripts
- `npm run dev` - Development with hot reload
- `npm run build` - TypeScript compilation
- `npm run start` - Production server
- `npm run clean` - Clean build artifacts

### Adding New Services

1. Add service URL to `config/index.ts`
2. Create route in `routes/`
3. Create controller in `controllers/`
4. Add route to main `index.ts`
5. Update health checks

## 🚨 Error Handling

All endpoints return standardized error responses:
```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "code": "ERROR_CODE",
    "statusCode": 400
  }
}
```

## 📈 Monitoring

Monitor service health via:
- `/health/detailed` endpoint
- Application logs
- Service response times

## 🔗 Dependencies

### Production
- `express` - Web framework
- `axios` - HTTP client for Python services
- `cors` - Cross-origin request handling
- `helmet` - Security middleware
- `morgan` - Request logging

### Development
- `typescript` - Type checking
- `ts-node-dev` - Development server
- Type definitions for all packages 