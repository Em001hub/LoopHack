import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import DecisionsTimelineCard from '../components/intelligence/DecisionsTimelineCard';
import UnansweredQuestionsCard from '../components/intelligence/UnansweredQuestionsCard';
import EntityNetworkCard from '../components/intelligence/EntityNetworkCard';

const ConversationIntelligence = () => {
    const [loading, setLoading] = useState(false);
    const [decisionsData, setDecisionsData] = useState(null);
    const [questionsData, setQuestionsData] = useState(null);
    const [entitiesData, setEntitiesData] = useState(null);
    const [error, setError] = useState(null);

    // Sample conversation data for demo
    const sampleMessages = [
        {
            user: 'alice@example.com',
            text: 'Should we use PostgreSQL or MongoDB for the new project?',
            timestamp: new Date(Date.now() - 3600000).toISOString()
        },
        {
            user: 'bob@example.com',
            text: 'We decided to go with PostgreSQL because it has better ACID compliance and our team has more experience with it.',
            timestamp: new Date(Date.now() - 3000000).toISOString()
        },
        {
            user: 'charlie@example.com',
            text: '@alice can you review PR-123? It implements the FastAPI authentication module.',
            timestamp: new Date(Date.now() - 2400000).toISOString()
        },
        {
            user: 'alice@example.com',
            text: 'Sure! How urgent is this? I have a blocker on PROJ-456.',
            timestamp: new Date(Date.now() - 1800000).toISOString()
        },
        {
            user: 'charlie@example.com',
            text: 'Not urgent, but would be great to get it in before the sprint ends.',
            timestamp: new Date(Date.now() - 1200000).toISOString()
        },
        {
            user: 'bob@example.com',
            text: "Let's also use React for the frontend and integrate with our existing Django backend.",
            timestamp: new Date(Date.now() - 600000).toISOString()
        },
        {
            user: 'david@example.com',
            text: 'We will implement the new feature using TypeScript and Next.js.',
            timestamp: new Date(Date.now() - 300000).toISOString()
        },
        {
            user: 'alice@example.com',
            text: 'What about the deployment strategy? Should we use Docker or Kubernetes?',
            timestamp: new Date(Date.now() - 60000).toISOString()
        }
    ];

    const analyzeConversation = async () => {
        setLoading(true);
        setError(null);

        try {
            const apiUrl = import.meta.env.VITE_INTELLIGENCE_API_URL || 'http://localhost:8002/api/v1';

            // Analyze decisions
            const decisionsResponse = await fetch(`${apiUrl}/conversation/analyze-decisions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    messages: sampleMessages,
                    min_confidence: 0.5
                })
            });
            const decisionsResult = await decisionsResponse.json();
            setDecisionsData(decisionsResult);

            // Analyze questions
            const questionsResponse = await fetch(`${apiUrl}/conversation/analyze-questions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    messages: sampleMessages,
                    min_confidence: 0.5
                })
            });
            const questionsResult = await questionsResponse.json();
            setQuestionsData(questionsResult);

            // Extract entities
            const entitiesResponse = await fetch(`${apiUrl}/conversation/extract-entities`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    messages: sampleMessages
                })
            });
            const entitiesResult = await entitiesResponse.json();
            setEntitiesData(entitiesResult);

        } catch (err) {
            console.error('Error analyzing conversation:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        analyzeConversation();
    }, []);

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-6">
            {/* Header */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-8"
            >
                <h1 className="text-4xl font-bold text-white mb-2 flex items-center gap-3">
                    <span className="text-5xl">💬</span>
                    Conversation Intelligence
                </h1>
                <p className="text-purple-300 text-lg">
                    AI-powered analysis of team conversations
                </p>
            </motion.div>

            {/* Error Display */}
            {error && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="mb-6 bg-red-900/40 border border-red-500/30 rounded-xl p-4"
                >
                    <div className="text-red-300 font-semibold mb-1">Error</div>
                    <div className="text-red-200 text-sm">{error}</div>
                </motion.div>
            )}

            {/* Controls */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mb-6 flex items-center gap-4"
            >
                <button
                    onClick={analyzeConversation}
                    disabled={loading}
                    className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold rounded-xl transition-all shadow-lg shadow-purple-500/30 disabled:shadow-none"
                >
                    {loading ? '🔄 Analyzing...' : '🔍 Analyze Conversation'}
                </button>
                <div className="text-purple-300 text-sm">
                    Analyzing {sampleMessages.length} messages
                </div>
            </motion.div>

            {/* Stats Overview */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6"
            >
                <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/20">
                    <div className="text-purple-300 text-sm mb-1">Messages</div>
                    <div className="text-white font-bold text-2xl">{sampleMessages.length}</div>
                </div>
                <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/20">
                    <div className="text-purple-300 text-sm mb-1">Decisions</div>
                    <div className="text-white font-bold text-2xl">
                        {decisionsData?.total_count || 0}
                    </div>
                </div>
                <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/20">
                    <div className="text-purple-300 text-sm mb-1">Questions</div>
                    <div className="text-white font-bold text-2xl">
                        {questionsData?.total_count || 0}
                    </div>
                </div>
                <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/20">
                    <div className="text-purple-300 text-sm mb-1">Entities</div>
                    <div className="text-white font-bold text-2xl">
                        {entitiesData ?
                            (entitiesData.entities.tasks?.length || 0) +
                            (entitiesData.entities.people?.length || 0) +
                            (entitiesData.entities.technologies?.length || 0)
                            : 0}
                    </div>
                </div>
            </motion.div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Decisions Timeline */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <DecisionsTimelineCard data={decisionsData} loading={loading} />
                </motion.div>

                {/* Unanswered Questions */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <UnansweredQuestionsCard data={questionsData} loading={loading} />
                </motion.div>

                {/* Entity Network - Full Width */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="lg:col-span-2"
                >
                    <EntityNetworkCard data={entitiesData} loading={loading} />
                </motion.div>
            </div>

            {/* Sample Conversation Display */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="mt-6 bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20"
            >
                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                    <span>💬</span>
                    Sample Conversation
                </h3>
                <div className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
                    {sampleMessages.map((msg, idx) => (
                        <div key={idx} className="bg-white/10 rounded-lg p-3 border border-white/20">
                            <div className="flex items-center gap-2 mb-1">
                                <span className="text-purple-300 font-semibold text-sm">
                                    {msg.user}
                                </span>
                                <span className="text-purple-400 text-xs">
                                    {new Date(msg.timestamp).toLocaleTimeString()}
                                </span>
                            </div>
                            <div className="text-white text-sm">{msg.text}</div>
                        </div>
                    ))}
                </div>
            </motion.div>
        </div>
    );
};

export default ConversationIntelligence;
