const express = require('express');
const router = express.Router();
const controller = require('../controllers/healthController');

router.get('/', controller.getHealthScores);

module.exports = router;
