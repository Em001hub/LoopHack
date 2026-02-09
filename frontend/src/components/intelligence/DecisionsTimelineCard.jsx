import { motion } from 'framer-motion';
import { format } from 'date-fns';

const DecisionsTimelineCard = ({ data, loading }) => {
    if (loading) {
        return (
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 h-full">
                <div className="animate-pulse space-y-3">
                    <div className="h-8 bg-white/20 rounded w-1/3 mb-4"></div>
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="h-20 bg-white/20 rounded"></div>
                    ))}
                </div>
            </div>
        );
    }

    const decisions = data?.decisions || [];
    const byType = data?.by_type || {};
    const totalCount = data?.total_count || 0;

    const getTypeColor = (type) => {
        const colors = {
            technical: 'from-purple-500/20 to-pink-500/20 border-purple-500/30',
            process: 'from-blue-500/20 to-cyan-500/20 border-blue-500/30',
            resource: 'from-green-500/20 to-emerald-500/20 border-green-500/30',
            timeline: 'from-orange-500/20 to-red-500/20 border-orange-500/30',
            scope: 'from-yellow-500/20 to-amber-500/20 border-yellow-500/30',
            general: 'from-gray-500/20 to-slate-500/20 border-gray-500/30'
        };
        return colors[type] || colors.general;
    };

    const getTypeIcon = (type) => {
        const icons = {
            technical: '⚙️',
            process: '🔄',
            resource: '👥',
            timeline: '📅',
            scope: '🎯',
            general: '💡'
        };
        return icons[type] || icons.general;
    };

    return (
        <motion.div
            whileHover={{ scale: 1.01 }}
            className="bg-gradient-to-br from-purple-900/40 to-pink-900/40 backdrop-blur-md rounded-2xl p-6 border border-purple-500/30 shadow-xl shadow-purple-500/20 h-full flex flex-col"
        >
            {/* Header */}
            <div className="mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    <span className="text-3xl">✅</span>
                    Decisions Made
                </h2>
                <p className="text-purple-300 text-sm mt-1">Team Decision Tracking</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-6">
                <div className="bg-white/10 rounded-xl p-3 border border-white/20">
                    <div className="text-purple-300 text-xs mb-1">Total Decisions</div>
                    <div className="text-white font-bold text-2xl">{totalCount}</div>
                </div>
                {Object.entries(byType).slice(0, 2).map(([type, count]) => (
                    <div key={type} className="bg-white/10 rounded-xl p-3 border border-white/20">
                        <div className="text-purple-300 text-xs mb-1 capitalize flex items-center gap-1">
                            <span>{getTypeIcon(type)}</span>
                            {type}
                        </div>
                        <div className="text-white font-bold text-2xl">{count}</div>
                    </div>
                ))}
            </div>

            {/* Decisions Timeline */}
            <div className="flex-1 overflow-y-auto custom-scrollbar space-y-3">
                {decisions.length === 0 ? (
                    <div className="text-center text-purple-300 py-8">
                        No decisions detected yet
                    </div>
                ) : (
                    decisions.slice(0, 10).map((decision, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className={`bg-gradient-to-r ${getTypeColor(decision.type)} backdrop-blur-sm rounded-xl p-4 border`}
                        >
                            <div className="flex items-start gap-3">
                                <div className="text-2xl flex-shrink-0">
                                    {getTypeIcon(decision.type)}
                                </div>
                                <div className="flex-1">
                                    <div className="text-white text-sm font-medium mb-2">
                                        {decision.decision}
                                    </div>
                                    <div className="flex flex-wrap items-center gap-2 text-xs">
                                        <span className="px-2 py-1 bg-white/10 rounded-full text-purple-200 capitalize">
                                            {decision.type}
                                        </span>
                                        <span className="text-purple-300">
                                            by {decision.decided_by}
                                        </span>
                                        <span className="text-purple-400">
                                            {decision.confidence && `${(decision.confidence * 100).toFixed(0)}% confidence`}
                                        </span>
                                    </div>
                                    {decision.rationale && (
                                        <div className="mt-2 text-xs text-purple-200 italic">
                                            💡 {decision.rationale}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </motion.div>
                    ))
                )}
            </div>

            {/* View All Link */}
            {decisions.length > 10 && (
                <div className="mt-4 text-center">
                    <button className="text-purple-300 hover:text-purple-100 text-sm font-medium">
                        View all {decisions.length} decisions →
                    </button>
                </div>
            )}
        </motion.div>
    );
};

export default DecisionsTimelineCard;
