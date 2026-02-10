module.exports = {
    broadcast: (io, room, event, data) => io.to(room).emit(event, data)
};
