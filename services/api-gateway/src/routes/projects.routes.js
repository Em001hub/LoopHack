const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const { INTEGRATION_SERVICE_URL } = require('../constants/services');
const router = express.Router();

// Jira endpoints
router.use('/jira', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/projects/jira': '/api/v1/jira',
    },
}));

// GitHub endpoints
router.use('/github', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/projects/github': '/api/v1/github',
    },
}));

// Slack endpoints
router.use('/slack', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/projects/slack': '/api/v1/slack',
    },
}));

// Google Calendar endpoints
router.use('/calendar', createProxyMiddleware({
    target: INTEGRATION_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api/projects/calendar': '/api/v1/calendar',
    },
}));

// Default - list all projects from all sources
router.get('/', async (req, res, next) => {
    try {
        const axios = require('axios');
        const allProjects = [];

        // Fetch from all sources (with error handling)
        const sources = ['jira', 'github', 'slack'];

        for (const source of sources) {
            try {
                const response = await axios.get(`${INTEGRATION_SERVICE_URL}/api/v1/${source}/projects`, {
                    timeout: 5000
                });
                allProjects.push(...response.data);
            } catch (err) {
                // Continue if one source fails
                console.warn(`Failed to fetch from ${source}:`, err.message);
            }
        }

        res.json(allProjects);
    } catch (error) {
        next(error);
    }
});

module.exports = router;
