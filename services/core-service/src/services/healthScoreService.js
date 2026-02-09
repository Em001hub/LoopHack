class HealthScoreService {
    async calculateAll() {
        return [{ projectId: 1, score: 90 }];
    }
}
module.exports = new HealthScoreService();
