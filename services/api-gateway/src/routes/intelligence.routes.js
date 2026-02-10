const express = require('express');
const router = express.Router();
// Proxy to Intelligence Service
router.post('/predict', (req, res) => res.send('Prediction proxy'));
module.exports = router;
