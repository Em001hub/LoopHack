class SlackSender {
    async send(channel, message) {
        console.log(`Sending slack to ${channel}`);
    }
}
module.exports = new SlackSender();
