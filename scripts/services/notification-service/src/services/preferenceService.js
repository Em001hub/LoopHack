class PreferenceService {
    async get(userId) {
        return { email: true, push: false };
    }
}
module.exports = new PreferenceService();
