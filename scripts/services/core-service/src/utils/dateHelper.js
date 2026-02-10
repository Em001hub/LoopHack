const { format } = require('date-fns');
module.exports = {
    now: () => format(new Date(), 'yyyy-MM-dd HH:mm:ss')
};
