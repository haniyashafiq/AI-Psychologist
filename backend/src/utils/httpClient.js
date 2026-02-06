/**
 * HTTP client for making requests to external services
 */
const axios = require('axios');
const logger = require('./logger');

/**
 * Create an HTTP client with default configuration
 */
const createHttpClient = (baseURL, timeout = 10000) => {
  const client = axios.create({
    baseURL,
    timeout,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Request interceptor
  client.interceptors.request.use(
    (config) => {
      logger.debug(`HTTP Request: ${config.method.toUpperCase()} ${config.url}`);
      return config;
    },
    (error) => {
      logger.error('HTTP Request Error:', error);
      return Promise.reject(error);
    }
  );

  // Response interceptor
  client.interceptors.response.use(
    (response) => {
      logger.debug(`HTTP Response: ${response.status} ${response.config.url}`);
      return response;
    },
    (error) => {
      if (error.response) {
        logger.error(`HTTP Response Error: ${error.response.status} ${error.config.url}`, {
          data: error.response.data,
        });
      } else if (error.request) {
        logger.error('HTTP No Response:', { url: error.config.url });
      } else {
        logger.error('HTTP Error:', error.message);
      }
      return Promise.reject(error);
    }
  );

  return client;
};

module.exports = { createHttpClient };
