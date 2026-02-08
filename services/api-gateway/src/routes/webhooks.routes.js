const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const { INTEGRATION_SERVICE_URL } = require('../constants/services');
const router = express.Router();

// Jira webhook
router.use('/jira', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/webhooks/jira': '/api/v1/jira/webhook',
    },
}));

// GitHub webhook
router.use('/github', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/webhooks/github': '/api/v1/github/webhook',
    },
}));

// Slack webhook
router.use('/slack', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/webhooks/slack': '/api/v1/slack/webhook',
    },
}));

// Google Calendar webhook
router.use('/calendar', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/webhooks/calendar': '/api/v1/calendar/webhook',
    },
}));

module.exports = router;
