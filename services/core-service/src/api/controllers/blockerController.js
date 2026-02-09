const service = require('../../services/blockerDetectionService');

exports.getBlockers = async (req, res) => {
    try {
        const blockers = await service.detectAll();
        res.json(blockers);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
