const axios = require('axios');
const config = require('../config/config');

/**
 * Axios instance for inter-service communication
 */
const httpClient = axios.create({
  timeout: config.serviceTimeout || 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add auth headers, logging
httpClient.interceptors.request.use(
  (config) => {
    // Add request ID for tracing
    config.headers['X-Request-ID'] = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    console.log(`[HTTP Client] ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[HTTP Client] Request error:', error.message);
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors, logging
httpClient.interceptors.response.use(
  (response) => {
    console.log(`[HTTP Client] Response ${response.status} from ${response.config.url}`);
    return response;
  },
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error(`[HTTP Client] Error ${error.response.status} from ${error.config.url}:`, error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error(`[HTTP Client] No response from ${error.config.url}`);
    } else {
      // Error in request setup
      console.error('[HTTP Client] Request setup error:', error.message);
    }
    return Promise.reject(error);
  }
);

module.exports = httpClient;
