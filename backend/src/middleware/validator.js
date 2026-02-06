/**
 * Request validation middleware using Joi
 */
const Joi = require('joi');

const assessmentSchema = Joi.object({
  text: Joi.string().min(10).max(5000).required().messages({
    'string.empty': 'Text cannot be empty',
    'string.min': 'Text must be at least 10 characters long',
    'string.max': 'Text cannot exceed 5000 characters',
    'any.required': 'Text is required',
  }),
  sessionId: Joi.string().uuid().optional(),
  metadata: Joi.object({
    timestamp: Joi.string().isoDate().optional(),
    userAgent: Joi.string().optional(),
  }).optional(),
});

const validateAssessment = (req, res, next) => {
  const { error, value } = assessmentSchema.validate(req.body, {
    abortEarly: false,
  });

  if (error) {
    error.isJoi = true;
    return next(error);
  }

  req.validatedBody = value;
  next();
};

module.exports = {
  validateAssessment,
};
