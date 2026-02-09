const express = require('express');
const router = express.Router();
const controller = require('../controllers/workloadController');

router.get('/', controller.getWorkload);

module.exports = router;
