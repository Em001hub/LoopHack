/**
 * React Hooks for Intelligence Service
 * Easy-to-use hooks for React applications
 */

import { useState, useEffect, useCallback } from 'react';

const API_BASE = process.env.REACT_APP_INTELLIGENCE_API || 'http://localhost:4002';

// ==================== CUSTOM HOOKS ====================

/**
 * Hook for timeline predictions
 * @param {string} projectId - Project ID
 * @param {object} options - Hook options
 */
export function usePrediction(projectId, options = {}) {
    const {
        autoRefresh = false,
        refreshInterval = 300000, // 5 minutes
        targetDate = null,
    } = options;

    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchPrediction = useCallback(async () => {
        if (!projectId) return;

        try {
            setLoading(true);
            setError(null);

            const response = await fetch(`${API_BASE}/api/v1/predict-timeline`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    project_id: projectId,
                    target_date: targetDate,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            setPrediction(data);
        } catch (err) {
            setError(err.message);
            console.error('Prediction fetch error:', err);
        } finally {
            setLoading(false);
        }
    }, [projectId, targetDate]);

    useEffect(() => {
        fetchPrediction();

        if (autoRefresh) {
            const interval = setInterval(fetchPrediction, refreshInterval);
            return () => clearInterval(interval);
        }
    }, [fetchPrediction, autoRefresh, refreshInterval]);

    return {
        prediction,
        loading,
        error,
        refetch: fetchPrediction,
    };
}

/**
 * Hook for user skills
 * @param {string} userId - User ID
 * @param {object} options - Hook options
 */
export function useSkills(userId, options = {}) {
    const {
        extractIfMissing = true,
        days = 90,
    } = options;

    const [skills, setSkills] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchSkills = useCallback(async () => {
        if (!userId) return;

        try {
            setLoading(true);
            setError(null);

            // Try to get cached skills first
            let response = await fetch(`${API_BASE}/api/v1/skills/${userId}`);

            // If not found and extractIfMissing is true, extract new skills
            if (!response.ok && response.status === 404 && extractIfMissing) {
                response = await fetch(`${API_BASE}/api/v1/extract-skills`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: userId,
                        days: days,
                    }),
                });
            }

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            setSkills(data);
        } catch (err) {
            setError(err.message);
            console.error('Skills fetch error:', err);
        } finally {
            setLoading(false);
        }
    }, [userId, extractIfMissing, days]);

    useEffect(() => {
        fetchSkills();
    }, [fetchSkills]);

    const extractSkills = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);

            const response = await fetch(`${API_BASE}/api/v1/extract-skills`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    days: days,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            setSkills(data);
            return data;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, [userId, days]);

    return {
        skills,
        loading,
        error,
        refetch: fetchSkills,
        extractSkills,
    };
}

/**
 * Hook for team sentiment
 * @param {string} projectId - Project ID
 * @param {object} options - Hook options
 */
export function useSentiment(projectId, options = {}) {
    const {
        autoRefresh = false,
        refreshInterval = 300000, // 5 minutes
        days = 30,
    } = options;

    const [sentiment, setSentiment] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchSentiment = useCallback(async () => {
        if (!projectId) return;

        try {
            setLoading(true);
            setError(null);

            const response = await fetch(
                `${API_BASE}/api/v1/team-morale/${projectId}?days=${days}`
            );

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            setSentiment(data);
        } catch (err) {
            setError(err.message);
            console.error('Sentiment fetch error:', err);
        } finally {
            setLoading(false);
        }
    }, [projectId, days]);

    useEffect(() => {
        fetchSentiment();

        if (autoRefresh) {
            const interval = setInterval(fetchSentiment, refreshInterval);
            return () => clearInterval(interval);
        }
    }, [fetchSentiment, autoRefresh, refreshInterval]);

    return {
        sentiment,
        loading,
        error,
        refetch: fetchSentiment,
    };
}

/**
 * Hook for Monte Carlo simulations
 * @param {string} projectId - Project ID
 * @param {object} scenarioParams - Scenario parameters
 */
export function useSimulation(projectId, scenarioParams = null) {
    const [simulation, setSimulation] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const runSimulation = useCallback(async (params = scenarioParams, nSimulations = 1000) => {
        if (!projectId) return;

        try {
            setLoading(true);
            setError(null);

            const response = await fetch(`${API_BASE}/api/v1/simulate-timeline`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    project_id: projectId,
                    n_simulations: nSimulations,
                    scenario_params: params,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            setSimulation(data);
            return data;
        } catch (err) {
            setError(err.message);
            console.error('Simulation error:', err);
            throw err;
        } finally {
            setLoading(false);
        }
    }, [projectId, scenarioParams]);

    return {
        simulation,
        loading,
        error,
        runSimulation,
    };
}

/**
 * Hook for daily insights
 * @param {string} projectId - Project ID
 * @param {object} options - Hook options
 */
export function useInsights(projectId, options = {}) {
    const {
        autoRefresh = false,
        refreshInterval = 600000, // 10 minutes
    } = options;

    const [insights, setInsights] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchInsights = useCallback(async () => {
        if (!projectId) return;

        try {
            setLoading(true);
            setError(null);

            const response = await fetch(`${API_BASE}/api/v1/daily-insights/${projectId}`);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            setInsights(data);
        } catch (err) {
            setError(err.message);
            console.error('Insights fetch error:', err);
        } finally {
            setLoading(false);
        }
    }, [projectId]);

    useEffect(() => {
        fetchInsights();

        if (autoRefresh) {
            const interval = setInterval(fetchInsights, refreshInterval);
            return () => clearInterval(interval);
        }
    }, [fetchInsights, autoRefresh, refreshInterval]);

    return {
        insights,
        loading,
        error,
        refetch: fetchInsights,
    };
}

/**
 * Hook for project health
 * @param {string} projectId - Project ID
 */
export function useProjectHealth(projectId) {
    const [health, setHealth] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchHealth = useCallback(async () => {
        if (!projectId) return;

        try {
            setLoading(true);
            setError(null);

            const response = await fetch(`${API_BASE}/api/v1/project-health/${projectId}`);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            setHealth(data);
        } catch (err) {
            setError(err.message);
            console.error('Health fetch error:', err);
        } finally {
            setLoading(false);
        }
    }, [projectId]);

    useEffect(() => {
        fetchHealth();
    }, [fetchHealth]);

    return {
        health,
        loading,
        error,
        refetch: fetchHealth,
    };
}

// ==================== EXAMPLE USAGE ====================

/*
// In your React component:

import { usePrediction, useSentiment, useInsights } from './hooks/useIntelligence';

function ProjectDashboard({ projectId }) {
    // Get timeline prediction
    const { prediction, loading: predLoading } = usePrediction(projectId, {
        autoRefresh: true,
        refreshInterval: 300000, // 5 min
    });

    // Get team sentiment
    const { sentiment, loading: sentLoading } = useSentiment(projectId, {
        autoRefresh: true,
    });

    // Get daily insights
    const { insights, loading: insightsLoading } = useInsights(projectId);

    if (predLoading || sentLoading || insightsLoading) {
        return <Loading />;
    }

    return (
        <div>
            <TimelineCard prediction={prediction} />
            <SentimentCard sentiment={sentiment} />
            <InsightsCard insights={insights} />
        </div>
    );
}

// Run simulation
function SimulationPanel({ projectId }) {
    const { simulation, loading, runSimulation } = useSimulation(projectId);

    const handleRunSimulation = () => {
        runSimulation({
            add_developers: 2,
            remove_features: 20,
        });
    };

    return (
        <div>
            <button onClick={handleRunSimulation} disabled={loading}>
                Run Simulation
            </button>
            {simulation && <SimulationResults data={simulation} />}
        </div>
    );
}
*/
