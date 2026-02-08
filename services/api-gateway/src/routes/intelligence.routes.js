const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const { INTELLIGENCE_SERVICE_URL } = require('../constants/services');
const router = express.Router();

router.use('/', createProxyMiddleware({
    target: INTELLIGENCE_SERVICE_URL,
    changeOrigin: true,
}));

module.exports = router;
