const express = require('express');
const router = express.Router();
const service = require('../../services/preferenceService');

router.get('/:userId', async (req, res) => {
    const prefs = await service.get(req.params.userId);
    res.json(prefs);
});

module.exports = router;
