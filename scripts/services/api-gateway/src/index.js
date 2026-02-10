const express = require('express');
const cors = require('cors');
const app = express();
const config = require('./config/config');
const routes = require('./routes');
const errorHandler = require('./middleware/errorHandler');

app.use(express.json());
app.use(cors());

// Routes
app.use('/api', routes);

// Error Handler
app.use(errorHandler);

app.listen(config.port, () => {
    console.log(`API Gateway running on port ${config.port}`);
});
