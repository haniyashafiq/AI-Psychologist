/**
 * Health check routes
 */
const express = require('express');
const router = express.Router();
const NLPService = require('../services/nlp.service');
const logger = require('../utils/logger');

const nlpService = new NLPService();

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

    const responseTime = Date.now() - startTime;
    const overallHealthy = nlpHealthy;

    res.status(overallHealthy ? 200 : 503).json({
      success: true,
      data: {
        status: overallHealthy ? 'healthy' : 'degraded',
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
        },
      },
    });
  } catch (error) {
    next(error);
  }
});

module.exports = router;
