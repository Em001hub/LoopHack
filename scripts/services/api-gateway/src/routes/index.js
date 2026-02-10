const express = require('express');
const router = express.Router();

const authRoutes = require('./auth.routes');
const projectRoutes = require('./projects.routes');
const intelligenceRoutes = require('./intelligence.routes');
const coreRoutes = require('./core.routes');
const healthRoutes = require('./health.routes');

router.use('/auth', authRoutes);
router.use('/projects', projectRoutes);
router.use('/intelligence', intelligenceRoutes);
router.use('/core', coreRoutes);
router.use('/health', healthRoutes);

module.exports = router;
