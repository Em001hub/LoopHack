require('dotenv').config();

module.exports = {
    PORT: process.env.PORT || 3000,
    NODE_ENV: process.env.NODE_ENV || 'development',
    JWT_SECRET: process.env.JWT_SECRET || 'your-super-secret-key',
    REDIS_URL: process.env.REDIS_URL || 'redis://localhost:6379',
};
