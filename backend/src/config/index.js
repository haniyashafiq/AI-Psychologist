/**
 * Application configuration
 */
require('dotenv').config({ path: `.env.${process.env.NODE_ENV || 'development'}` });

/**
 * Helper function to ensure URL has protocol
 * Render provides hostnames without protocol, so we add https:// in production
 */
function ensureProtocol(url, isProduction) {
  if (!url) return url;
  // If URL already has protocol, return as-is
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url;
  }
  // In production, use https. In development, use http
  const protocol = isProduction ? 'https://' : 'http://';
  return protocol + url;
}

const isProduction = process.env.NODE_ENV === 'production';

module.exports = {
  port: process.env.PORT || 3000,
  nodeEnv: process.env.NODE_ENV || 'development',
  nlpService: {
    url: ensureProtocol(process.env.NLP_SERVICE_URL || 'localhost:8000', isProduction),
    timeout: parseInt(process.env.NLP_SERVICE_TIMEOUT) || 10000,
  },
  ragService: {
    url: ensureProtocol(process.env.RAG_SERVICE_URL || 'localhost:8001', isProduction),
    timeout: parseInt(process.env.RAG_SERVICE_TIMEOUT) || 60000,
  },
  cors: {
    origin: ensureProtocol(process.env.CORS_ORIGIN || 'localhost:5173', isProduction),
  },
  logging: {
    level: process.env.LOG_LEVEL || 'info',
  },
  rateLimit: {
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
  },
};
