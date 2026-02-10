/**
 * RAG Service client for communicating with Python RAG service
 */
const { createHttpClient } = require('../utils/httpClient');
const config = require('../config');
const logger = require('../utils/logger');

class RAGService {
  constructor() {
    this.client = createHttpClient(config.ragService.url, config.ragService.timeout);
  }

  /**
   * Send patient text + NLP symptoms to the RAG service for AI clinical assessment
   */
  async queryAssessment(text, symptoms = null, metadata = null) {
    try {
      logger.info('Calling RAG service for AI clinical assessment');

      const payload = { text };
      if (symptoms) payload.symptoms = symptoms;
      if (metadata) payload.metadata = metadata;

      const response = await this.client.post('/rag/query', payload);

      if (!response.data.success) {
        throw new Error('RAG service returned unsuccessful response');
      }

      logger.info('RAG service assessment received successfully');
      return response.data.data;
    } catch (error) {
      logger.error('Failed to get RAG assessment:', {
        message: error.message,
        code: error.code,
        status: error.response?.status,
      });

      const cleanError = new Error(
        error.response?.data?.detail || error.message || 'Failed to communicate with RAG service'
      );
      cleanError.statusCode = error.response?.status || 503;
      cleanError.isAxiosError = error.isAxiosError;
      cleanError.code = error.code;
      throw cleanError;
    }
  }

  /**
   * Check RAG service health
   */
  async healthCheck() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      logger.error('RAG service health check failed:', {
        message: error.message,
        code: error.code,
      });
      const cleanError = new Error('RAG service health check failed');
      cleanError.statusCode = error.response?.status || 503;
      throw cleanError;
    }
  }
}

module.exports = RAGService;
