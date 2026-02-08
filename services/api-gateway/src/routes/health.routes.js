const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.json({
        status: 'UP',
        service: 'api-gateway',
        timestamp: new Date().toISOString(),
    });
});

module.exports = router;
