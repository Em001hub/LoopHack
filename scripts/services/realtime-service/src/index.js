const { Server } = require('socket.io');
const connection = require('./sockets/connection');

const io = new Server(3000, {
    cors: { origin: "*" }
});

io.on('connection', (socket) => {
    connection(io, socket);
});

console.log('Realtime service running on 3000');
