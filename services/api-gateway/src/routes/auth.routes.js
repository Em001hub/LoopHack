const express = require('express');
const router = express.Router();

// Mock auth endpoints
router.post('/login', (req, res) => {
    res.json({ message: 'Login successful', token: 'mock-jwt-token' });
});

router.post('/register', (req, res) => {
    res.json({ message: 'Registration successful' });
});

module.exports = router;
