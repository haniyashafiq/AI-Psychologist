/**
 * Express application configuration
 */
const express = require('express');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const config = require('./config');
const corsMiddleware = require('./middleware/cors');
const errorHandler = require('./middleware/errorHandler');
const assessmentRoutes = require('./routes/assessment.routes');
const healthRoutes = require('./routes/health.routes');
const logger = require('./utils/logger');

const app = express();

// Security middleware
app.use(helmet());

// Rate limiting
const limiter = rateLimit(config.rateLimit);
app.use('/api/', limiter);

// Body parsing
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true }));

// CORS
app.use(corsMiddleware);

// HTTP request logging
if (config.nodeEnv === 'development') {
  app.use(morgan('dev'));
} else {
  app.use(
    morgan('combined', {
      stream: {
        write: (message) => logger.info(message.trim()),
      },
    })
  );
}

// Routes
app.get('/', (req, res) => {
  res.json({
    service: 'AI Psychologist Backend API',
    version: '1.0.0',
    status: 'running',
    endpoints: {
      health: '/api/v1/health',
      assessment: '/api/v1/assessment',
      analyze: 'POST /api/v1/assessment/analyze',
    },
  });
});

app.use('/api/v1/health', healthRoutes);
app.use('/api/v1/assessment', assessmentRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: {
      message: 'Route not found',
      path: req.path,
    },
  });
});

// Error handling
app.use(errorHandler);

module.exports = app;
