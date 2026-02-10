class AlertService {
    async create(data) {
        return { id: 1, ...data };
    }
}
module.exports = new AlertService();
