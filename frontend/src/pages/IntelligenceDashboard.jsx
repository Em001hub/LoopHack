import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import TimelinePredictionCard from '../components/intelligence/TimelinePredictionCard';
import SentimentAnalysisCard from '../components/intelligence/SentimentAnalysisCard';
import ProjectInsightsCard from '../components/intelligence/ProjectInsightsCard';
import MonteCarloSimulation from '../components/intelligence/MonteCarloSimulation';
import RiskFactorsCard from '../components/intelligence/RiskFactorsCard';
import { intelligenceService } from '../services/intelligenceService';
import {
    transformSentimentData,
    transformPredictionData,
    transformInsightsData,
    transformSimulationData
} from '../utils/dataAdapters';

const IntelligenceDashboard = () => {
    const [projectId, setProjectId] = useState('proj_alpha');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [refreshInterval, setRefreshInterval] = useState(30000); // 30 seconds

    const [predictionData, setPredictionData] = useState(null);
    const [sentimentData, setSentimentData] = useState(null);
    const [insightsData, setInsightsData] = useState(null);
    const [simulationData, setSimulationData] = useState(null);

    const fetchAllData = async () => {
        try {
            setLoading(true);
            setError(null);

            const [predictions, sentiment, insights] = await Promise.all([
                intelligenceService.predictTimeline(projectId),
                intelligenceService.getTeamSentiment(projectId),
                intelligenceService.getProjectInsights(projectId)
            ]);

            // Transform API data to component format
            setPredictionData(transformPredictionData(predictions));
            setSentimentData(transformSentimentData(sentiment));
            setInsightsData(transformInsightsData(insights));
        } catch (err) {
            console.error('Error fetching intelligence data:', err);
            setError(err.message || 'Failed to fetch data');
        } finally {
            setLoading(false);
        }
    };

    const runSimulation = async () => {
        try {
            const result = await intelligenceService.runSimulation(projectId, {
                n_simulations: 1000,
                scenario_params: {}
            });
            // Transform simulation data
            setSimulationData(transformSimulationData(result));
        } catch (err) {
            console.error('Error running simulation:', err);
        }
    };

    useEffect(() => {
        fetchAllData();

        // Auto-refresh
        const interval = setInterval(fetchAllData, refreshInterval);
        return () => clearInterval(interval);
    }, [projectId, refreshInterval]);

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: { y: 20, opacity: 0 },
        visible: {
            y: 0,
            opacity: 1,
            transition: {
                type: 'spring',
                stiffness: 100
            }
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
            {/* Header */}
            <motion.div
                initial={{ y: -20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className="mb-8"
            >
                <div className="flex items-center justify-between mb-4">
                    <div>
                        <h1 className="text-4xl font-bold text-white mb-2 flex items-center gap-3">
                            <span className="text-5xl">🧠</span>
                            Intelligence Dashboard
                        </h1>
                        <p className="text-purple-300 text-lg">
                            AI-Powered Project Analytics & Predictions
                        </p>
                    </div>

                    <div className="flex items-center gap-4">
                        {/* Project Selector */}
                        <div className="bg-white/10 backdrop-blur-md rounded-xl px-4 py-2 border border-white/20">
                            <label className="text-purple-200 text-sm block mb-1">Project</label>
                            <select
                                value={projectId}
                                onChange={(e) => setProjectId(e.target.value)}
                                className="bg-transparent text-white font-semibold outline-none cursor-pointer"
                            >
                                <option value="proj_alpha">Project Alpha</option>
                                <option value="proj_beta">Project Beta</option>
                                <option value="proj_gamma">Project Gamma</option>
                            </select>
                        </div>

                        {/* Refresh Button */}
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={fetchAllData}
                            className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-xl font-semibold shadow-lg hover:shadow-purple-500/50 transition-shadow"
                        >
                            🔄 Refresh
                        </motion.button>

                        {/* Run Simulation Button */}
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={runSimulation}
                            className="bg-gradient-to-r from-cyan-500 to-blue-500 text-white px-6 py-3 rounded-xl font-semibold shadow-lg hover:shadow-cyan-500/50 transition-shadow"
                        >
                            🎲 Run Simulation
                        </motion.button>
                    </div>
                </div>

                {/* Status Bar */}
                <div className="flex items-center gap-4 text-sm">
                    <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${loading ? 'bg-yellow-400 animate-pulse' : 'bg-green-400'}`} />
                        <span className="text-purple-200">
                            {loading ? 'Updating...' : 'Live'}
                        </span>
                    </div>
                    <span className="text-purple-300">
                        Last updated: {new Date().toLocaleTimeString()}
                    </span>
                    {error && (
                        <span className="text-red-400">⚠️ {error}</span>
                    )}
                </div>
            </motion.div>

            {/* Main Dashboard Grid */}
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6"
            >
                {/* Timeline Prediction - Takes 2 columns on XL screens */}
                <motion.div variants={itemVariants} className="xl:col-span-2">
                    <TimelinePredictionCard
                        data={predictionData}
                        loading={loading}
                        projectId={projectId}
                    />
                </motion.div>

                {/* Sentiment Analysis */}
                <motion.div variants={itemVariants}>
                    <SentimentAnalysisCard
                        data={sentimentData}
                        loading={loading}
                    />
                </motion.div>

                {/* Risk Factors */}
                <motion.div variants={itemVariants}>
                    <RiskFactorsCard
                        data={predictionData?.risk_factors || []}
                        loading={loading}
                    />
                </motion.div>

                {/* Project Insights - Takes 2 columns */}
                <motion.div variants={itemVariants} className="lg:col-span-2">
                    <ProjectInsightsCard
                        data={insightsData}
                        loading={loading}
                    />
                </motion.div>

                {/* Monte Carlo Simulation - Full width */}
                {simulationData && (
                    <motion.div
                        variants={itemVariants}
                        className="lg:col-span-2 xl:col-span-3"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                    >
                        <MonteCarloSimulation
                            data={simulationData}
                            projectId={projectId}
                        />
                    </motion.div>
                )}
            </motion.div>

            {/* Footer Stats */}
            <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4"
            >
                <div className="bg-white/5 backdrop-blur-md rounded-xl p-4 border border-white/10">
                    <div className="text-purple-300 text-sm mb-1">Prediction Accuracy</div>
                    <div className="text-2xl font-bold text-white">87%</div>
                </div>
                <div className="bg-white/5 backdrop-blur-md rounded-xl p-4 border border-white/10">
                    <div className="text-purple-300 text-sm mb-1">Avg Response Time</div>
                    <div className="text-2xl font-bold text-white">~200ms</div>
                </div>
                <div className="bg-white/5 backdrop-blur-md rounded-xl p-4 border border-white/10">
                    <div className="text-purple-300 text-sm mb-1">Model Inference</div>
                    <div className="text-2xl font-bold text-white">&lt;50ms</div>
                </div>
                <div className="bg-white/5 backdrop-blur-md rounded-xl p-4 border border-white/10">
                    <div className="text-purple-300 text-sm mb-1">Throughput</div>
                    <div className="text-2xl font-bold text-white">100+ req/s</div>
                </div>
            </motion.div>
        </div>
    );
};

export default IntelligenceDashboard;
