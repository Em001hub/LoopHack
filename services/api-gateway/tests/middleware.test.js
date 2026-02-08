const errorHandler = require('../src/middleware/errorHandler');
const logger = require('../src/middleware/logger');

describe('Middleware Tests', () => {
    describe('Error Handler', () => {
        it('should handle errors with status code', () => {
            const err = new Error('Test error');
            err.statusCode = 400;

            const req = {};
            const res = {
                status: jest.fn().mockReturnThis(),
                json: jest.fn()
            };
            const next = jest.fn();

            errorHandler(err, req, res, next);

            expect(res.status).toHaveBeenCalledWith(400);
            expect(res.json).toHaveBeenCalledWith(
                expect.objectContaining({
                    error: expect.any(String)
                })
            );
        });

        it('should default to 500 for unknown errors', () => {
            const err = new Error('Unknown error');

            const req = {};
            const res = {
                status: jest.fn().mockReturnThis(),
                json: jest.fn()
            };
            const next = jest.fn();

            errorHandler(err, req, res, next);

            expect(res.status).toHaveBeenCalledWith(500);
        });
    });

    describe('Logger Middleware', () => {
        it('should log request details', () => {
            const req = {
                method: 'GET',
                path: '/test',
                ip: '127.0.0.1'
            };
            const res = {};
            const next = jest.fn();

            logger(req, res, next);

            expect(next).toHaveBeenCalled();
        });
    });
});
