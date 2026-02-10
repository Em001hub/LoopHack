const Queue = require('bull');
const blockerQueue = new Queue('blocker-scanner');

blockerQueue.process(async (job) => {
    // Background blocker scanning
});
module.exports = blockerQueue;
