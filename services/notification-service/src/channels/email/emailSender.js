class EmailSender {
    async send(to, content) {
        console.log(`Sending email to ${to}`);
    }
}
module.exports = new EmailSender();
