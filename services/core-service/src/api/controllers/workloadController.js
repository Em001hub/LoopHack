const service = require('../../services/workloadService');

exports.getWorkload = async (req, res) => {
    try {
        const workload = await service.calculateWorkload();
        res.json(workload);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
