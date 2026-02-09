const queue = require('../config/queue');

class NotificationService {
    async send(data) {
        await queue.add(data);
    }
}
module.exports = new NotificationService();
