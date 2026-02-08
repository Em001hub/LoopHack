const httpClient = require('./httpClient');
const SERVICES = require('../constants/services');

/**
 * Service Registry - Manages service discovery and health checks
 */
class ServiceRegistry {
  constructor() {
    this.services = SERVICES;
    this.healthStatus = {};
  }

  /**
   * Get service URL by name
   */
  getServiceUrl(serviceName) {
    const service = this.services[serviceName];
    if (!service) {
      throw new Error(`Service ${serviceName} not found in registry`);
    }
    return service.url;
  }

  /**
   * Check health of a specific service
   */
  async checkServiceHealth(serviceName) {
    try {
      const serviceUrl = this.getServiceUrl(serviceName);
      const response = await httpClient.get(`${serviceUrl}/health`, {
        timeout: 5000,
      });
   