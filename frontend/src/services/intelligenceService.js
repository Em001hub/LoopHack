import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_INTELLIGENCE_API_URL || 'http://localhost:8002/api/v1';

class IntelligenceService {
    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            timeout: 30000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

    /**
     * Predict project timeline completion
     */
    async predictTimeline(projectId, targetDate = null) {
        try {
            const response = await this.client.post('/predict-timeline', {
                project_id: projectId,
                target_date: targetDate
            });
            return response.data;
        } catch (error) {
            console.error('Error predicting timeline:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Get prediction history for a project
     */
    async getPredictionHistory(projectId) {
        try {
            const response = await this.client.get(`/prediction-history/${projectId}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching prediction history:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Get team sentiment analysis
     */
    async getTeamSentiment(projectId, days = 7) {
        try {
            const response = await this.client.get(`/team-sentiment/${projectId}`, {
                params: { days }
            });
            return response.data;
        } catch (error) {
            console.error('Error fetching team sentiment:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Analyze sentiment of text
     */
    async analyzeSentiment(text, context = 'general') {
        try {
            const response = await this.client.post('/analyze-sentiment', {
                text,
                context
            });
            return response.data;
        } catch (error) {
            console.error('Error analyzing sentiment:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Get project insights
     */
    async getProjectInsights(projectId) {
        try {
            const response = await this.client.get(`/project-insights/${projectId}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching project insights:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Get team insights
     */
    async getTeamInsights(teamId) {
        try {
            const response = await this.client.get(`/team-insights/${teamId}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching team insights:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Run Monte Carlo simulation
     */
    async runSimulation(projectId, params = {}) {
        try {
            const response = await this.client.post('/run-simulation', {
                project_id: projectId,
                n_simulations: params.n_simulations || 1000,
                scenario_params: params.scenario_params || {}
            });
            return response.data;
        } catch (error) {
            console.error('Error running simulation:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Compare multiple scenarios
     */
    async compareScenarios(projectId, scenarios, nSimulations = 500) {
        try {
            const response = await this.client.post('/compare-scenarios', {
                project_id: projectId,
                scenarios,
                n_simulations: nSimulations
            });
            return response.data;
        } catch (error) {
            console.error('Error comparing scenarios:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Get simulation history
     */
    async getSimulationHistory(projectId) {
        try {
            const response = await this.client.get(`/simulation-history/${projectId}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching simulation history:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Extract skills from text
     */
    async extractSkills(text, context = 'general') {
        try {
            const response = await this.client.post('/extract-skills', {
                text,
                context
            });
            return response.data;
        } catch (error) {
            console.error('Error extracting skills:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Get skill recommendations for a project
     */
    async getSkillRecommendations(projectId) {
        try {
            const response = await this.client.get(`/skill-recommendations/${projectId}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching skill recommendations:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Get risk analysis for a project
     */
    async getRiskAnalysis(projectId) {
        try {
            const response = await this.client.get(`/risk-analysis/${projectId}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching risk analysis:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Analyze conversation intelligence
     */
    async analyzeConversation(text) {
        try {
            const response = await this.client.post('/conversation-intelligence', null, {
                params: { text }
            });
            return response.data;
        } catch (error) {
            console.error('Error analyzing conversation:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Get detailed health check
     */
    async getHealthDetailed() {
        try {
            const response = await this.client.get('/health-detailed');
            return response.data;
        } catch (error) {
            console.error('Error fetching health:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Get model performance metrics
     */
    async getModelPerformance() {
        try {
            const response = await this.client.get('/model-performance');
            return response.data;
        } catch (error) {
            console.error('Error fetching model performance:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Recalculate timeline for a project
     */
    async recalculateTimeline(projectId) {
        try {
            const response = await this.client.post(`/recalculate-timeline/${projectId}`);
            return response.data;
        } catch (error) {
            console.error('Error recalculating timeline:', error);
            throw this.handleError(error);
        }
    }

    /**
     * Handle API errors
     */
    handleError(error) {
        if (error.response) {
            // Server responded with error
            return new Error(error.response.data.detail || error.response.data.message || 'Server error');
        } else if (error.request) {
            // Request made but no response
            return new Error('No response from server. Please check if the Intelligence Service is running.');
        } else {
            // Something else happened
            return new Error(error.message || 'An unexpected error occurred');
        }
    }
}

export const intelligenceService = new IntelligenceService();
export default intelligenceService;
