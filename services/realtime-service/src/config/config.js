require('dotenv').config();
module.exports = {
    redisUrl: process.env.REDIS_URL,
    openaiKey: process.env.OPENAI_API_KEY
};
