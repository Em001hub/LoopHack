class DigestService {
    async createDailyDigest() {
        return { summary: "Good progress today" };
    }
}
module.exports = new DigestService();
