/**
 * Assessment routes
 */
const express = require('express');
const router = express.Router();
const { validateAssessment } = require('../middleware/validator');
const assessmentController = require('../controllers/assessment.controller');

// POST /api/v1/assessment/analyze - Analyze symptoms and diagnose
router.post('/analyze', validateAssessment, assessmentController.analyzeSymptoms);

// GET /api/v1/assessment - Get assessment info
router.get('/', assessmentController.getInfo);

module.exports = router;
