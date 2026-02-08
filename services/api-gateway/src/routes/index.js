const express = require('express');
const router = express.Router();

const authRoutes = require('./auth.routes');
const projectRoutes = require('./projects.routes');
const intelligenceRoutes = require('./intelligence.routes');
const coreRoutes = require('./core.routes');
const healthRoutes = require('./health.routes');
const webhooksRoutes = require('./webhooks.routes');
const syncRoutes = require('./sync.routes');

// Public routes
router.use('/health', healthRoutes);
router.use('/auth', authRoutes);

// Webhook routes (should validate signatures in production)
router.use('/webhooks', webhooksRoutes);

// Protected routes (could add auth middleware here)
router.use('/projects', projectRoutes);
router.use('/intelligence', intelligenceRoutes);
router.use('/core', coreRoutes);
router.use('/sync', syncRoutes);

module.exports = router;
