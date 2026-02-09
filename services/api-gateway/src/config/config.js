require('dotenv').config();

module.exports = {
    port: process.env.PORT || 3000,
    redisUrl: process.env.REDIS_URL,
    jwtSecret: process.env.JWT_SECRET,
    services: {
        integration: process.env.INTEGRATION_SERVICE_URL || 'http://localhost:8001',
        intelligence: process.env.INTELLIGENCE_SERVICE_URL || 'http://localhost:8002',
        core: process.env.CORE_SERVICE_URL || 'http://localhost:8003',
        notification: process.env.NOTIFICATION_SERVICE_URL || 'http://localhost:8005'
    }
};
