/**
 * Global error handling middleware
 */
const logger = require('../utils/logger');

const errorHandler = (err, req, res, next) => {
  logger.error('Error occurred:', {
    message: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
  });

  // Joi validation error
  if (err.isJoi) {
    return res.status(400).json({
      success: false,
      error: {
        message: 'Validation error',
        details: err.details.map((detail) => detail.message),
      },
    });
  }

  // Axios error (from NLP service)
  if (err.isAxiosError) {
    if (err.response) {
      return res.status(err.response.status).json({
        success: false,
        error: {
          message: 'NLP service error',
          details: err.response.data,
        },
      });
    } else if (err.code === 'ECONNREFUSED') {
      return res.status(503).json({
        success: false,
        error: {
          message: 'NLP service unavailable',
          details: 'Could not connect to NLP service',
        },
      });
    }
  }

  // Default error
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal server error';

  res.status(statusCode).json({
    success: false,
    error: {
      message,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
    },
  });
};

module.exports = errorHandler;
