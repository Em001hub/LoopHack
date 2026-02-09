import { motion } from 'framer-motion';

const ProjectInsightsCard = ({ data, loading }) => {
    if (loading) {
        return (
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 h-full">
                <div className="animate-pulse space-y-3">
                    <div className="h-8 bg-white/20 rounded w-1/3 mb-4"></div>
                    {[1, 2, 3, 4].map((i) => (
                        <div key={i} className="h-16 bg-white/20 rounded"></div>
                    ))}
                </div>
            </div>
        );
    }

    // Default insights if none provided
    const insights = data?.insights || [
        'Team velocity has increased by 15% over the past sprint',
        'Consider allocating more resources to the authentication module',
        'Code review turnaround time is optimal at 4.2 hours',
        'Technical debt is within acceptable limits',
        'Sprint burndown indicates healthy progress'
    ];

    const categories = data?.categories || {
        performance: 2,
        resources: 1,
        quality: 1,
        progress: 1
    };

    const getCategoryIcon = (category) => {
        const icons = {
            performance: '⚡',
            resources: '👥',
            quality: '✨',
            progress: '📈',
            risk: '⚠️',
            optimization: '🎯'
        };
        return icons[category] || '💡';
    };

    const getCategoryColor = (category) => {
        const colors = {
            performance: 'from-yellow-500/20 to-orange-500/20 border-yellow-500/30',
            resources: 'from-blue-500/20 to-cyan-500/20 border-blue-500/30',
            quality: 'from-purple-500/20 to-pink-500/20 border-purple-500/30',
            progress: 'from-green-500/20 to-emerald-500/20 border-green-500/30',
            risk: 'from-red-500/20 to-orange-500/20 border-red-500/30',
            optimization: 'from-indigo-500/20 to-purple-500/20 border-indigo-500/30'
        };
        return colors[category] || 'from-gray-500/20 to-slate-500/20 border-gray-500/30';
    };

    const insightsWithCategories = insights.map((insight, idx) => {
        // Simple categorization based on keywords
        let category = 'optimization';
        if (insight.toLowerCase().includes('velocity') || insight.toLowerCase().includes('performance')) {
            category = 'performance';
        } else if (insight.toLowerCase().includes('resource') || insight.toLowerCase().includes('team')) {
            category = 'resources';
        } else if (insight.toLowerCase().includes('quality') || insight.toLowerCase().includes('code')) {
            category = 'quality';
        } else if (insight.toLowerCase().includes('progress') || insight.toLowerCase().includes('sprint')) {
            category = 'progress';
        } else if (insight.toLowerCase().includes('risk') || insight.toLowerCase().includes('delay')) {
            category = 'risk';
        }
        return { text: insight, category, id: idx };
    });

    return (
        <motion.div
            whileHover={{ scale: 1.01 }}
            className="bg-gradient-to-br from-cyan-900/40 to-blue-900/40 backdrop-blur-md rounded-2xl p-6 border border-cyan-500/30 shadow-xl shadow-cyan-500/20 h-full"
        >
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                        <span className="text-3xl">💡</span>
                        AI Insights
                    </h2>
                    <p className="text-cyan-300 text-sm mt-1">Actionable Recommendations</p>
                </div>

                <div className="bg-white/10 rounded-xl px-4 py-2 border border-white/20">
                    <div className="text-cyan-200 text-xs">Total Insights</div>
                    <div className="text-white font-bold text-lg">{insights.length}</div>
                </div>
            </div>

            {/* Category Summary */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
                {Object.entries(categories).map(([category, count]) => (
                    <div
                        key={category}
                        className="bg-white/5 rounded-lg p-3 border border-white/10 text-center"
                    >
                        <div className="text-2xl mb-1">{getCategoryIcon(category)}</div>
                        <div className="text-white font-bold text-lg">{count}</div>
                        <div className="text-cyan-300 text-xs capitalize">{category}</div>
                    </div>
                ))}
            </div>

            {/* Insights List */}
            <div className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
                {insightsWithCategories.map((item, idx) => (
                    <motion.div
                        key={item.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: idx * 0.1 }}
                        className={`bg-gradient-to-r ${getCategoryColor(item.category)} backdrop-blur-sm rounded-xl p-4 border`}
                    >
                        <div className="flex items-start gap-3">
                            <div className="text-2xl flex-shrink-0">
                                {getCategoryIcon(item.category)}
                            </div>
                            <div className="flex-1">
                                <div className="text-white text-sm leading-relaxed">
                                    {item.text}
                                </div>
                                <div className="mt-2 flex items-center gap-2">
                                    <span className="text-xs px-2 py-1 bg-white/10 rounded-full text-cyan-200 capitalize">
                                        {item.category}
                                    </span>
                                    {data?.confidence_scores && data.confidence_scores[idx] && (
                                        <span className="text-xs text-cyan-300">
                                            {(data.confidence_scores[idx] * 100).toFixed(0)}% confidence
                                        </span>
                                    )}
                                </div>
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>

            {/* Action Required */}
            {data?.action_required && data.action_required.length > 0 && (
                <div className="mt-4 bg-gradient-to-r from-orange-900/30 to-red-900/30 rounded-xl p-4 border border-orange-500/30">
                    <h3 className="text-orange-300 font-semibold mb-2 flex items-center gap-2">
                        <span>🚨</span>
                        Action Required
                    </h3>
                    <ul className="space-y-2">
                        {data.action_required.map((action, idx) => (
                            <li key={idx} className="text-orange-100 text-sm flex items-start gap-2">
                                <span className="text-orange-400 mt-1">•</span>
                                <span>{action}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </motion.div>
    );
};

export default ProjectInsightsCard;
