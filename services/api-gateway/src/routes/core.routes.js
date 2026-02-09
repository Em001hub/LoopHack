const express = require('express');
const router = express.Router();
// Proxy to Core Service
router.get('/stats', (req, res) => res.send('Core stats proxy'));
module.exports = router;
