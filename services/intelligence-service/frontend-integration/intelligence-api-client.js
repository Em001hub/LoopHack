/**
 * Intelligence Service API Client
 * JavaScript/TypeScript client for integrating with the Intelligence Service
 */

class IntelligenceAPI {
    constructor(baseURL = 'http://localhost:4002') {
        this.baseURL = baseURL;
        this.headers = {
            'Content-Type': 'application/json',
        };
    }

    /**
     * Make HTTP request
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        const config = {
            ...options,
            headers: {
                ...this.headers,
                ...options.headers,
            },
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    }

    // ==================== PREDICTION ENDPOINTS ====================

    /**
     * Predict project timeline
     * @param {string} projectId - Project ID
     * @param {string} targetDate - Optional target completion date (ISO format)
     */
    async predictTimeline(projectId, targetDate = null) {
        return this.request('/api/v1/predict-timeline', {
            method: 'POST',
            body: JSON.stringify({
                project_id: projectId,
                target_date: targetDate,
            }),
        });
    }

    /**
     * Get prediction history
     * @param {string} projectId - Project ID
     * @param {number} limit - Number of records to fetch
     */
    async getPredictionHistory(projectId, limit = 10) {
        return this.request(`/api/v1/prediction-history/${projectId}?limit=${limit}`);
    }

    /**
     * Trigger background recalculation
     * @param {string} projectId - Project ID
     */
    async recalculateTimeline(projectId) {
        return this.request(`/api/v1/recalculate-timeline/${projectId}`, {
            method: 'POST',
        });
    }

    // ==================== SKILL ENDPOINTS ====================

    /**
     * Extract user skills
     * @param {string} userId - User ID
     * @param {number} days - Days of history to analyze
     */
    async extractSkills(userId, days = 90) {
        return this.request('/api/v1/extract-skills', {
            method: 'POST',
            body: JSON.stringify({
                user_id: userId,
                days: days,
            }),
        });
    }

    /**
     * Get cached user skills
     * @param {string} userId - User ID
     */
    async getUserSkills(userId) {
        return this.request(`/api/v1/skills/${userId}`);
    }

    /**
     * Match task to user
     * @param {string} userId - User ID
     * @param {string} taskId - Task ID
     * @param {object} requirements - Task requirements
     */
    async matchTask(userId, taskId, requirements) {
        return this.request('/api/v1/match-task', {
            method: 'POST',
            body: JSON.stringify({
                user_id: userId,
                task_id: taskId,
                task_requirements: requirements,
            }),
        });
    }

    /**
     * Get team skill matrix
     * @param {string} projectId - Project ID
     */
    async getTeamSkillMatrix(projectId) {
        return this.request(`/api/v1/team-skills/${projectId}`);
    }

    /**
     * Get task assignment recommendations
     * @param {string} taskId - Task ID
     */
    async recommendAssignment(taskId) {
        return this.request(`/api/v1/recommend-assignment/${taskId}`, {
            method: 'POST',
        });
    }

    // ==================== SIMULATION ENDPOINTS ====================

    /**
     * Run Monte Carlo simulation
     * @param {string} projectId - Project ID
     * @param {number} nSimulations - Number of simulations
     * @param {object} scenarioParams - Scenario parameters
     */
    async simulateTimeline(projectId, nSimulations = 1000, scenarioParams = null) {
        return this.request('/api/v1/simulate-timeline', {
            method: 'POST',
            body: JSON.stringify({
                project_id: projectId,
                n_simulations: nSimulations,
                scenario_params: scenarioParams,
            }),
        });
    }

    /**
     * Compare multiple scenarios
     * @param {string} projectId - Project ID
     * @param {array} scenarios - Array of scenario objects
     * @param {number} nSimulations - Number of simulations
     */
    async compareScenarios(projectId, scenarios, nSimulations = 1000) {
        return this.request('/api/v1/compare-scenarios', {
            method: 'POST',
            body: JSON.stringify({
                project_id: projectId,
                scenarios: scenarios,
                n_simulations: nSimulations,
            }),
        });
    }

    /**
     * Run what-if analysis
     * @param {string} projectId - Project ID
     * @param {object} params - What-if parameters
     */
    async whatIfAnalysis(projectId, params = {}) {
        const queryParams = new URLSearchParams(params).toString();
        return this.request(`/api/v1/what-if/${projectId}?${queryParams}`, {
            method: 'POST',
        });
    }

    // ==================== SENTIMENT ENDPOINTS ====================

    /**
     * Analyze user sentiment
     * @param {string} userId - User ID
     * @param {number} days - Days to analyze
     */
    async analyzeUserSentiment(userId, days = 30) {
        return this.request('/api/v1/analyze-user', {
            method: 'POST',
            body: JSON.stringify({
                user_id: userId,
                days: days,
            }),
        });
    }

    /**
     * Get team morale
     * @param {string} projectId - Project ID
     * @param {number} days - Days to analyze
     */
    async getTeamMorale(projectId, days = 30) {
        return this.request(`/api/v1/team-morale/${projectId}?days=${days}`);
    }

    /**
     * Check burnout risk
     * @param {string} userId - User ID
     */
    async getBurnoutRisk(userId) {
        return this.request(`/api/v1/burnout-risk/${userId}`);
    }

    /**
     * Get sentiment alerts
     * @param {string} projectId - Project ID
     */
    async getSentimentAlerts(projectId) {
        return this.request(`/api/v1/sentiment-alerts/${projectId}`);
    }

    // ==================== HEALTH & INSIGHTS ====================

    /**
     * Get project health score
     * @param {string} projectId - Project ID
     */
    async getProjectHealth(projectId) {
        return this.request(`/api/v1/project-health/${projectId}`);
    }

    /**
     * Get daily insights
     * @param {string} projectId - Project ID
     */
    async getDailyInsights(projectId) {
        return this.request(`/api/v1/daily-insights/${projectId}`);
    }

    /**
     * Get task recommendations
     * @param {string} taskId - Task ID
     */
    async getTaskRecommendations(taskId) {
        return this.request(`/api/v1/recommendations/${taskId}`);
    }

    // ==================== HEALTH CHECK ====================

    /**
     * Check service health
     */
    async healthCheck() {
        return this.request('/health');
    }
}

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = IntelligenceAPI;
}

if (typeof window !== 'undefined') {
    window.IntelligenceAPI = IntelligenceAPI;
}

// Example usage:
/*
const api = new IntelligenceAPI('http://localhost:4002');

// Predict timeline
const prediction = await api.predictTimeline('proj_alpha', '2024-03-15T00:00:00Z');
console.log('Predicted completion:', prediction.predicted_completion_date);

// Get team morale
const morale = await api.getTeamMorale('proj_alpha');
console.log('Team morale:', morale.team_morale.label);

// Run simulation
const simulation = await api.simulateTimeline('proj_alpha', 1000);
console.log('Median weeks:', simulation.predicted_weeks.median);

// Get daily insights
const insights = await api.getDailyInsights('proj_alpha');
console.log('Summary:', insights.summary);
*/
