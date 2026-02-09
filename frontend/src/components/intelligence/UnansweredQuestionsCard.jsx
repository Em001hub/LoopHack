import { motion } from 'framer-motion';

const UnansweredQuestionsCard = ({ data, loading }) => {
    if (loading) {
        return (
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 h-full">
                <div className="animate-pulse space-y-3">
                    <div className="h-8 bg-white/20 rounded w-1/3 mb-4"></div>
                    {[1, 2].map((i) => (
                        <div key={i} className="h-16 bg-white/20 rounded"></div>
                    ))}
                </div>
            </div>
        );
    }

    const questions = data?.questions || [];
    const unansweredCount = data?.unanswered_count || 0;
    const alerts = data?.alerts || [];
    const totalCount = data?.total_count || 0;

    const unanswered = questions.filter(q => !q.is_answered);

    const getUrgencyColor = (urgency) => {
        const colors = {
            high: 'from-red-500/20 to-orange-500/20 border-red-500/30',
            medium: 'from-yellow-500/20 to-amber-500/20 border-yellow-500/30',
            low: 'from-blue-500/20 to-cyan-500/20 border-blue-500/30'
        };
        return colors[urgency] || colors.low;
    };

    const getUrgencyBadge = (urgency) => {
        const badges = {
            high: 'bg-red-500/20 text-red-300 border-red-500/30',
            medium: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
            low: 'bg-blue-500/20 text-blue-300 border-blue-500/30'
        };
        return badges[urgency] || badges.low;
    };

    const getTypeIcon = (type) => {
        const icons = {
            technical: '🔧',
            clarification: '❓',
            status: '📊',
            permission: '✋',
            information: 'ℹ️',
            general: '💬'
        };
        return icons[type] || icons.general;
    };

    return (
        <motion.div
            whileHover={{ scale: 1.01 }}
            className="bg-gradient-to-br from-orange-900/40 to-red-900/40 backdrop-blur-md rounded-2xl p-6 border border-orange-500/30 shadow-xl shadow-orange-500/20 h-full flex flex-col"
        >
            {/* Header */}
            <div className="mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    <span className="text-3xl">❓</span>
                    Unanswered Questions
                </h2>
                <p className="text-orange-300 text-sm mt-1">Questions Needing Attention</p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-3 mb-6">
                <div className="bg-white/10 rounded-xl p-3 border border-white/20 text-center">
                    <div className="text-orange-300 text-xs mb-1">Total</div>
                    <div className="text-white font-bold text-2xl">{totalCount}</div>
                </div>
                <div className="bg-white/10 rounded-xl p-3 border border-white/20 text-center">
                    <div className="text-orange-300 text-xs mb-1">Answered</div>
                    <div className="text-green-400 font-bold text-2xl">{totalCount - unansweredCount}</div>
                </div>
                <div className="bg-white/10 rounded-xl p-3 border border-white/20 text-center">
                    <div className="text-orange-300 text-xs mb-1">Unanswered</div>
                    <div className="text-red-400 font-bold text-2xl">{unansweredCount}</div>
                </div>
            </div>

            {/* Alerts */}
            {alerts.length > 0 && (
                <div className="mb-4 bg-gradient-to-r from-red-900/30 to-orange-900/30 rounded-xl p-3 border border-red-500/30">
                    <div className="text-red-300 font-semibold mb-2 flex items-center gap-2">
                        <span>🚨</span>
                        {alerts.length} Alert{alerts.length > 1 ? 's' : ''}
                    </div>
                    <div className="text-red-200 text-xs">
                        {alerts[0].recommended_action}
                    </div>
                </div>
            )}

            {/* Questions List */}
            <div className="flex-1 overflow-y-auto custom-scrollbar space-y-3">
                {unanswered.length === 0 ? (
                    <div className="text-center text-orange-300 py-8">
                        <div className="text-4xl mb-2">🎉</div>
                        <div>All questions answered!</div>
                    </div>
                ) : (
                    unanswered.slice(0, 8).map((question, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className={`bg-gradient-to-r ${getUrgencyColor(question.urgency)} backdrop-blur-sm rounded-xl p-4 border`}
                        >
                            <div className="flex items-start gap-3">
                                <div className="text-2xl flex-shrink-0">
                                    {getTypeIcon(question.type)}
                                </div>
                                <div className="flex-1">
                                    <div className="text-white text-sm mb-2">
                                        {question.question}
                                    </div>
                                    <div className="flex flex-wrap items-center gap-2 text-xs">
                                        <span className={`px-2 py-1 rounded-full border ${getUrgencyBadge(question.urgency)} capitalize`}>
                                            {question.urgency} urgency
                                        </span>
                                        <span className="px-2 py-1 bg-white/10 rounded-full text-orange-200 capitalize">
                                            {question.type}
                                        </span>
                                        <span className="text-orange-300">
                                            by {question.asker}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    ))
                )}
            </div>

            {/* Summary */}
            {unanswered.length > 0 && (
                <div className="mt-4 text-center text-xs text-orange-300">
                    {unanswered.filter(q => q.urgency === 'high').length > 0 && (
                        <div className="text-red-300 font-semibold">
                            ⚠️ {unanswered.filter(q => q.urgency === 'high').length} high-priority question{unanswered.filter(q => q.urgency === 'high').length > 1 ? 's' : ''} need immediate attention
                        </div>
                    )}
                </div>
            )}
        </motion.div>
    );
};

export default UnansweredQuestionsCard;
