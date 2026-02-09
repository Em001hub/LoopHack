const express = require('express');
const router = express.Router();
const controller = require('../controllers/blockerController');

router.get('/', controller.getBlockers);

module.exports = router;
