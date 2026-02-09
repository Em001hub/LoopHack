class ReportService {
    async generateReport() {
        return { pdfUrl: "http://..." };
    }
}
module.exports = new ReportService();
