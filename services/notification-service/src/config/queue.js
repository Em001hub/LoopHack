const Queue = require('bull');
const config = require('./config');

const notificationQueue = new Queue('notifications', config.redisUrl);

module.exports = notificationQueue;
