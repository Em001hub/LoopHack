const cors = require('cors');
module.exports = cors({
    origin: '*', // Configure as needed
    optionsSuccessStatus: 200
});
