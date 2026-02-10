class RoutingService {
    async route(notification, user) {
        return ['email', 'inapp'];
    }
}
module.exports = new RoutingService();
