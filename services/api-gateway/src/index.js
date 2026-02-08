const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());

// Service Endpoints Configuration
const services = {
    integration: process.env.INTEGRATION_SERVICE_URL || 'http://localhost:8000',
    core: process.env.CORE_SERVICE_URL || 'http://localhost:3001',
    intelligence: process.env.INTELLIGENCE_SERVICE_URL || 'http://localhost:8001',
    realtime: process.env.REALTIME_SERVICE_URL || 'http://localhost:3002',
};

// Health Check
app.get('/health', (req, res) => {
    res.json({
        status: 'UP',
        service: 'api-gateway',
        timestamp: new Date().toISOString(),
    });
});

// Proxy Routes
// Integration Service
app.use('/api/integrations', createProxyMiddleware({
    target: services.integration,
    changeOrigin: true,
    pathRewrite: {
        '^/api/integrations': '/api/v1',
    },
}));

// Core Logic Service
app.use('/api/core', createProxyMiddleware({
    target: services.core,
    changeOrigin: true,
    pathRewrite: {
        '^/api/core': '/api/v1',
    },
}));

// Intelligence Service
app.use('/api/intelligence', createProxyMiddleware({
    target: services.intelligence,
    changeOrigin: true,
    pathRewrite: {
        '^/api/intelligence': '/api/v1',
    },
}));

// Error Handling Middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        error: 'Internal Server Error',
        message: err.message,
    });
});

// Start Server
app.listen(PORT, () => {
    console.log(`🚀 API Gateway running on port ${PORT}`);
    console.log(`🔗 Proxying /api/integrations -> ${services.integration}`);
});
