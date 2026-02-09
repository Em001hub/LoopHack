class WorkloadService {
    async calculateWorkload() {
        return [{ userId: 1, load: 80 }];
    }
}
module.exports = new WorkloadService();
