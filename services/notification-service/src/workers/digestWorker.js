const Queue = require('bull');
const digestQueue = new Queue('digest-notifications');

digestQueue.process(async (job) => {
    // Process digest
});
