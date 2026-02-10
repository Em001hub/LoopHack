const express = require('express');
const app = express();
const config = require('./config/config');

const notificationRoutes = require('./api/routes/notifications.routes');
const preferenceRoutes = require('./api/routes/preferences.routes');

app.use(express.json());

app.use('/notifications', notificationRoutes);
app.use('/preferences', preferenceRoutes);

app.listen(config.port, () => {
    console.log(`Notification Service running on port ${config.port}`);
});
