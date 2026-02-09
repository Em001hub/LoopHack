const express = require('express');
const router = express.Router();
const service = require('../../services/notificationService');

router.post('/send', async (req, res) => {
    await service.send(req.body);
    res.send('Sent');
});

module.exports = router;
