const express = require('express');
const helmet = require('helmet');
const { PORT } = require('./config/config');
const corsMiddleware = require('./middleware/cors');
const loggerMiddleware = require('./middleware/logger');
const rateLimiterMiddleware = require('./middleware/rateLimiter');
const errorHandler = require('./middleware/errorHandler');
const routes = require('./routes');

const app = express();

// Security Middleware
app.use(helmet());
app.use(corsMiddleware);

// Request Logging
app.use(loggerMiddleware);

// Rate Limiting
app.use(rateLimiterMiddleware);

// Body Parsing
app.use(express.json());

// Main Routes
app.use('/api', routes);

// Global Error Handler
app.use(errorHandler);

app.listen(PORT, () => {
    console.log(`API Gateway running on port ${PORT}`);
});
