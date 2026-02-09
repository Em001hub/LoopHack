const chatHandler = require('../chat/chatHandler');

module.exports = (io, socket) => {
    console.log('User connected:', socket.id);

    socket.on('chat:message', (msg) => chatHandler(io, socket, msg));

    socket.on('disconnect', () => {
        console.log('User disconnected:', socket.id);
    });
};
