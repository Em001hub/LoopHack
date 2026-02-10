const service = require('../../services/alertService');

exports.createAlert = async (req, res) => {
    try {
        const alert = await service.create(req.body);
        res.status(201).json(alert);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
