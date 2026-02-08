const express = require('express');
const router = express.Router();

const authRoutes = require('./auth.routes');
const projectRoutes = require('./projects.routes');
const intelligenceRoutes = require('./intelligence.routes');
const coreRoutes = require('./core.routes');
const healthRoutes = require('./health.routes');

// Public routes
router.use('/health', healthRoutes);
router.use('/auth', authRoutes);

// Protected routes (could add auth middleware here)
router.use('/projects', projectRoutes);
router.use('/intelligence', intelligenceRoutes);
router.use('/core', coreRoutes);

module.exports = router;
