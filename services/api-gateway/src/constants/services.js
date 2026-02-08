module.exports = {
    INTEGRATION_SERVICE_URL: process.env.INTEGRATION_SERVICE_URL || 'http://localhost:8000',
    CORE_SERVICE_URL: process.env.CORE_SERVICE_URL || 'http://localhost:3001',
    INTELLIGENCE_SERVICE_URL: process.env.INTELLIGENCE_SERVICE_URL || 'http://localhost:8001',
    REALTIME_SERVICE_URL: process.env.REALTIME_SERVICE_URL || 'http://localhost:3002',
};
