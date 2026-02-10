/**
 * Health check routes
 */
const express = require('express');
const router = express.Router();
const NLPService = require('../services/nlp.service');
const RAGService = require('../services/rag.service');
const logger = require('../utils/logger');

const nlpService = new NLPService();
const ragService = new RAGService();

// GET /api/v1/health - Health check
router.get('/', async (req, res, next) => {
  try {
    const startTime = Date.now();

    // Check NLP service health
    let nlpHealthy = false;
    let nlpError = null;

    try {
      await nlpService.healthCheck();
      nlpHealthy = true;
    } catch (error) {
      nlpError = error.message;
      logger.warn('NLP service health check failed:', error);
    }

    // Check RAG service health
    let ragHealthy = false;
    let ragError = null;
    let ragDetails = null;

    try {
      ragDetails = await ragService.healthCheck();
      ragHealthy = true;
    } catch (error) {
      ragError = error.message;
      logger.warn('RAG service health check failed:', error);
    }

    const responseTime = Date.now() - startTime;
    // System requires both NLP and RAG services to be fully healthy
    const overallHealthy = nlpHealthy && ragHealthy;
    const degraded = nlpHealthy || ragHealthy;

    let status = 'unhealthy';
    if (overallHealthy) status = 'healthy';
    else if (degraded) status = 'degraded';

    res.status(overallHealthy ? 200 : 503).json({
      success: true,
      data: {
        status,
        service: 'backend-api',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        responseTime,
        dependencies: {
          nlpService: {
            status: nlpHealthy ? 'healthy' : 'unhealthy',
            error: nlpError,
          },
          ragService: {
            status: ragHealthy ? 'healthy' : 'unhealthy',
            error: ragError,
            details: ragDetails,
          },
        },
      },
    });
  } catch (error) {
    next(error);
  }
});

module.exports = router;
