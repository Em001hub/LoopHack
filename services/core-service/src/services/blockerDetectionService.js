class BlockerDetectionService {
    async detectAll() {
        return [{ id: 1, reason: "Dependency missing" }];
    }
}
module.exports = new BlockerDetectionService();
