const nlp = require('./nlpProcessor');
const executor = require('./queryExecutor');
const generator = require('./responseGenerator');

module.exports = async (io, socket, msg) => {
    // 1. Process intent
    const intent = await nlp.process(msg);
    // 2. Execute query
    const data = await executor.execute(intent);
    // 3. Generate response
    const response = await generator.generate(data);

    socket.emit('chat:response', response);
};
