/**
 * Application configuration
 */
require('dotenv').config({ path: `.env.${process.env.NODE_ENV || 'development'}` });

module.exports = {
  port: process.env.PORT || 3000,
  nodeEnv: process.env.NODE_ENV || 'development',
  nlpService: {
    url: process.env.NLP_SERVICE_URL || 'http://localhost:8000',
    timeout: parseInt(process.env.NLP_SERVICE_TIMEOUT) || 10000,
  },
  ragService: {
    url: process.env.RAG_SERVICE_URL || 'http://localhost:8001',
    timeout: parseInt(process.env.RAG_SERVICE_TIMEOUT) || 60000,
  },
  cors: {
    origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  },
  logging: {
    level: process.env.LOG_LEVEL || 'info',
  },
  rateLimit: {
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
  },
};
