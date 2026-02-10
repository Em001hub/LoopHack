const queue = require('../config/queue');
const sender = require('../channels/email/emailSender');

queue.process(async (job) => {
    await sender.send(job.data.to, job.data.content);
});
