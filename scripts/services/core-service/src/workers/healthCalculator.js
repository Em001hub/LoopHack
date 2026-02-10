const Queue = require('bull');
const healthQueue = new Queue('health-calculator');

healthQueue.process(async (job) => {
    // Background health calculation
});
module.exports = healthQueue;
