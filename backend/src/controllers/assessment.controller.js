/**
 * Assessment controller handling diagnosis requests
 */
const { v4: uuidv4 } = require('uuid');
const DiagnosisService = require('../services/diagnosis.service');
const logger = require('../utils/logger');

const diagnosisService = new DiagnosisService();

/**
 * Analyze patient symptoms and return diagnosis
 */
const analyzeSymptoms = async (req, res, next) => {
  const requestId = uuidv4();
  const startTime = Date.now();

  try {
    const { text } = req.validatedBody;
    const sessionId = req.validatedBody.sessionId || requestId;

    logger.info(`Assessment request ${requestId}`, {
      sessionId,
      textLength: text.length,
    });

    // Perform diagnosis
    const result = await diagnosisService.diagnose(text);

    // Calculate total processing time
    const totalTime = Date.now() - startTime;

    logger.info(`Assessment completed ${requestId}`, {
      sessionId,
      duration: totalTime,
      meetsThreshold: result.diagnosis.meetsThreshold,
      severity: result.severity.level,
    });

    // Send response
    res.status(200).json({
      success: true,
      data: {
        sessionId,
        requestId,
        diagnosis: result.diagnosis,
        severity: result.severity,
        symptoms: result.symptoms,
        recommendations: result.recommendations,
        disclaimer: result.disclaimer,
      },
      timestamp: new Date().toISOString(),
      processingTime: totalTime,
    });
  } catch (error) {
    logger.error(`Assessment failed ${requestId}:`, error);
    next(error);
  }
};

/**
 * Get assessment system information
 */
const getInfo = async (req, res, next) => {
  try {
    res.json({
      success: true,
      data: {
        service: 'Depression Diagnosis Assessment API',
        version: '1.0.0',
        capabilities: {
          disorder: 'Major Depressive Disorder',
          criteria: 'DSM-5',
          features: [
            'Natural language symptom extraction',
            'Rule-based diagnostic matching',
            'Severity assessment',
            'Functional impairment detection',
            'Crisis detection',
          ],
        },
        endpoints: {
          analyze: 'POST /api/v1/assessment/analyze',
          health: 'GET /api/v1/health',
        },
      },
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  analyzeSymptoms,
  getInfo,
};
