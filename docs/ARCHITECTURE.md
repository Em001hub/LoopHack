# System Architecture

## Overview
Microservices architecture with the following components:

- **Frontend**: React/Vite application
- **API Gateway**: Entry point (Node.js/Express)
- **Integration Service**: External tool integrations (Python/FastAPI)
- **Intelligence Service**: AI/ML capabilities (Python/FastAPI)
- **Core Service**: Business logic (Node.js)
- **Realtime Service**: WebSockets (Node.js/Socket.io)
- **Notification Service**: Alerts and notifications (Node.js)

## Data Storage
- PostgreSQL for relational data
- Redis for caching and pub/sub
