const service = require('../../services/healthScoreService');

exports.getHealthScores = async (req, res) => {
    try {
        const scores = await service.calculateAll();
        res.json(scores);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
