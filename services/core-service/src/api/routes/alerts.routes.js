const express = require('express');
const router = express.Router();
const controller = require('../controllers/alertController');

router.post('/', controller.createAlert);

module.exports = router;
