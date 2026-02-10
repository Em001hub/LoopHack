module.exports = {
    join: (socket, room) => socket.join(room),
    leave: (socket, room) => socket.leave(room)
};
