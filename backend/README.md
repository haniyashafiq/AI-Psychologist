# Backend API - Depression Diagnosis

Express.js REST API server for the depression diagnosis system. Handles diagnosis requests, communicates with the NLP service, and applies DSM-5 MDD diagnostic criteria.

## Setup

### Prerequisites

- Node.js 18+
- npm

### Installation

1. Install dependencies:

```bash
npm install
```

2. Configure environment:

```bash
cp .env.development .env
# Edit .env if needed
```

3. Ensure NLP service is running on `http://localhost:8000`

### Running the Server

```bash
# Development mode (with auto-reload)
npm run dev

# Production mode
npm start
```

The API will be available at `http://localhost:3000`

## API Endpoints

### Health Check

```bash
GET /api/v1/health
```

Response:

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "dependencies": {
      "nlpService": { "status": "healthy" }
    }
  }
}
```

### Analyze Symptoms

```bash
POST /api/v1/assessment/analyze
Content-Type: application/json

{
  "text": "I feel sad and empty most of the time. I can't sleep at night, have no energy, and feel worthless. Nothing interests me anymore."
}
```

Response:

```json
{
  "success": true,
  "data": {
    "diagnosis": {
      "condition": "Major Depressive Disorder",
      "meetsThreshold": true,
      "confidence": "high",
      "criteriaMetCount": 5,
      "requiredCount": 5
    },
    "severity": {
      "level": "moderate",
      "score": 5,
      "functionalImpairment": false
    },
    "symptoms": [...],
    "recommendations": [...],
    "disclaimer": "..."
  }
}
```

## Features

- **DSM-5 MDD Diagnostic Engine**: Implements complete diagnostic criteria
- **Severity Assessment**: Calculates mild/moderate/severe with functional impairment
- **Crisis Detection**: Flags suicidal ideation for immediate intervention
- **Comprehensive Recommendations**: Based on diagnosis and severity
- **Error Handling**: Graceful degradation if NLP service unavailable
- **Rate Limiting**: Prevents abuse (100 requests per 15 minutes)
- **Security**: Helmet.js, CORS, input validation

## Architecture

```
Request → Validation → NLP Service → Diagnosis Engine → Severity Calculator → Response
```

## Testing

```bash
npm test

# Watch mode
npm run test:watch
```

## Environment Variables

- `PORT`: Server port (default: 3000)
- `NODE_ENV`: Environment (development/production)
- `NLP_SERVICE_URL`: NLP service URL
- `NLP_SERVICE_TIMEOUT`: Timeout for NLP requests (ms)
- `CORS_ORIGIN`: Allowed CORS origin
- `LOG_LEVEL`: Logging level (debug/info/warn/error)
