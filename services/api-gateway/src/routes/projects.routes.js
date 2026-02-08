const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const { INTEGRATION_SERVICE_URL } = require('../constants/services');
const router = express.Router();

router.use('/', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/projects': '/api/v1/jira/projects', // Example rewrite
    },
}));

module.exports = router;
