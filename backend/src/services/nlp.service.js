/**
 * NLP Service client for communicating with Python NLP service
 */
const { createHttpClient } = require('../utils/httpClient');
const config = require('../config');
const logger = require('../utils/logger');

class NLPService {
  constructor() {
    this.client = createHttpClient(config.nlpService.url, config.nlpService.timeout);
  }

  /**
   * Extract symptoms from natural language text
   * @param {string} text - Patient symptom description
   * @returns {Promise} Extracted symptoms and metadata
   */
  async extractSymptoms(text) {
    try {
      logger.info('Calling NLP service to extract symptoms');

      const response = await this.client.post('/nlp/extract-symptoms', {
        text,
        context: {
          language: 'en',
          preprocessing_options: {
            remove_punctuation: false,
            lowercase: false,
            lemmatize: true,
          },
        },
      });

      if (!response.data.success) {
        throw new Error('NLP service returned unsuccessful response');
      }

      logger.info(`NLP service extracted ${response.data.data.summary.unique_symptoms} symptoms`);

      return response.data.data;
    } catch (error) {
      logger.error('Failed to extract symptoms from NLP service:', {
        message: error.message,
        code: error.code,
        status: error.response?.status,
      });

      // Create a clean error without circular references
      const cleanError = new Error(
        error.response?.data?.error?.message ||
          error.message ||
          'Failed to communicate with NLP service'
      );
      cleanError.statusCode = error.response?.status || 503;
      cleanError.isAxiosError = error.isAxiosError;
      cleanError.code = error.code;

      throw cleanError;
    }
  }

  /**
   * Health check for NLP service
   * @returns {Promise} Service health status
   */
  async healthCheck() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      logger.error('NLP service health check failed:', {
        message: error.message,
        code: error.code,
      });

      const cleanError = new Error('NLP service health check failed');
      cleanError.statusCode = error.response?.status || 503;
      throw cleanError;
    }
  }
}

module.exports = NLPService;
