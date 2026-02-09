const express = require('express');
const router = express.Router();
// Proxy to Integration Service
router.get('/', (req, res) => res.send('Projects proxy'));
module.exports = router;
