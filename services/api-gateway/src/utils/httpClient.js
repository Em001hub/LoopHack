const axios = require('axios');
const instance = axios.create({
    timeout: 5000,
});
module.exports = instance;
