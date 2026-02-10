const express = require('express');
const app = express();
const config = require('./config/config');

// Routes will be imported here
const healthRoutes = require('./api/routes/health-scores.routes');
const blockerRoutes = require('./api/routes/blockers.routes');
const workloadRoutes = require('./api/routes/workload.routes');
const alertRoutes = require('./api/routes/alerts.routes');
const insightRoutes = require('./api/routes/insights.routes');

app.use(express.json());

app.use('/health-scores', healthRoutes);
app.use('/blockers', blockerRoutes);
app.use('/workload', workloadRoutes);
app.use('/alerts', alertRoutes);
app.use('/insights', insightRoutes);

app.listen(config.port, () => {
    console.log(`Core Service running on port ${config.port}`);
});
