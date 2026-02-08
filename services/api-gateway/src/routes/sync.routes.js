const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const { INTEGRATION_SERVICE_URL } = require('../constants/services');
const router = express.Router();

// Trigger sync for all integrations
router.post('/all', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/sync/all': '/api/v1/sync/all',
    },
}));

// Trigger Jira sync
router.post('/jira', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/sync/jira': '/api/v1/jira/sync',
    },
}));

// Trigger GitHub sync
router.post('/github', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/sync/github': '/api/v1/github/sync',
    },
}));

// Trigger Slack sync
router.post('/slack', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/sync/slack': '/api/v1/slack/sync',
    },
}));

// Trigger Calendar sync
router.post('/calendar', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/sync/calendar': '/api/v1/calendar/sync',
    },
}));

// Get sync status
router.get('/status', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/sync/status': '/api/v1/sync/status',
    },
}));

module.exports = router;
