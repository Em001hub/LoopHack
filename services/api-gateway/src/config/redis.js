const Redis = require('ioredis');
const config = require('./config');

const redis = new Redis(config.redisUrl);

redis.on('connect', () => {
    console.log('Redis connected');
});

redis.on('error', (err) => {
    console.error('Redis error', err);
});

module.exports = redis;
