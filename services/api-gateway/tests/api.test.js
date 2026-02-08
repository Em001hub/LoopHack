const request = require('supertest');
const express = require('express');
const routes = require('../src/routes');
const errorHandler = require('../src/middleware/errorHandler');

// Create test app
const app = express();
app.use(express.json());
app.use('/api', routes);
app.use(errorHandler);

describe('API Gateway Routes', () => {
    describe('Health Check', () => {
        it('should return 200 for health endpoint', async () => {
            const res = await request(app).get('/api/health');
            expect(res.statusCode).toBe(200);
            expect(res.body).toHaveProperty('status');
        });
    });

    describe('Auth Routes', () => {
        it('should have auth routes registered', async () => {
            const res = await request(app).post('/api/auth/login');
            // Should not be 404 (route exists)
            expect(res.statusCode).not.toBe(404);
        });
    });

    describe('Project Routes', () => {
        it('should proxy to integration service', async () => {
            const res = await request(app).get('/api/projects');
            // Route should exist (may fail due to no backend, but not 404)
            expect(res.statusCode).not.toBe(404);
        });
    });

    describe('Intelligence Routes', () => {
        it('should have intelligence routes registered', async () => {
            const res = await request(app).get('/api/intelligence');
            expect(res.statusCode).not.toBe(404);
        });
    });

    describe('Core Routes', () => {
        it('should have core routes registered', async () => {
            const res = await request(app).get('/api/core');
            expect(res.statusCode).not.toBe(404);
        });
    });
});
