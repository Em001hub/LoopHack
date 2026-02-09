const Queue = require('bull');
const digestQueue = new Queue('digest-generator');

digestQueue.process(async (job) => {
    // Background digest generation
});
module.exports = digestQueue;
