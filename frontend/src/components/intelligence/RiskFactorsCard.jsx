import { motion } from 'framer-motion';

const RiskFactorsCard = ({ data, loading }) => {
    if (loading) {
        return (
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 h-full">
                <div className="animate-pulse space-y-3">
                    <div className="h-8 bg-white/20 rounded w-2/3 mb-4"></div>
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="h-20 bg-white/20 rounded"></div>
                    ))}
                </div>
            </div>
        );
    }

    // Default risks if none provided
    const risks = Array.isArray(data) && data.length > 0 ? data : [
        {
            factor: 'High complexity tasks pending',
            severity: 'high',
            impact: 'May delay completion by 1-2 weeks',
            mitigation: 'Break down into smaller tasks'
        },
        {
            factor: 'Team velocity below average',
            severity: 'medium',
            impact: 'Reduced sprint output',
            mitigation: 'Review team capacity and blockers'
        },
        {
            factor: 'Multiple blocked tasks',
            severity: 'medium',
            impact: 'Dependencies causing delays',
            mitigation: 'Prioritize unblocking critical path items'
        }
    ];

    // Parse risks if they're strings
    const parsedRisks = risks.map((risk, idx) => {
        if (typeof risk === 'string') {
            // Simple risk string
            let severity = 'medium';
            if (risk.toLowerCase().includes('critical') || risk.toLowerCase().includes('urgent')) {
                severity = 'high';
            } else if (risk.toLowerCase().includes('minor') || risk.toLowerCase().includes('low')) {
                severity = 'low';
            }

            return {
                factor: risk,
                severity,
                impact: 'Impact analysis pending',
                mitigation: 'Review and assess mitigation strategies',
                id: idx
            };
        }
        return { ...risk, id: idx };
    });

    const getSeverityColor = (severity) => {
        switch (severity?.toLowerCase()) {
            case 'high':
            case 'critical':
                return {
                    bg: 'from-red-900/40 to-orange-900/40',
                    border: 'border-red-500/40',
                    text: 'text-red-400',
                    badge: 'bg-red-500/20 text-red-300 border-red-500/30'
                };
            case 'medium':
                return {
                    bg: 'from-yellow-900/40 to-orange-900/40',
                    border: 'border-yellow-500/40',
                    text: 'text-yellow-400',
                    badge: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30'
                };
            case 'low':
                return {
                    bg: 'from-blue-900/40 to-cyan-900/40',
                    border: 'border-blue-500/40',
                    text: 'text-blue-400',
                    badge: 'bg-blue-500/20 text-blue-300 border-blue-500/30'
                };
            default:
                return {
                    bg: 'from-gray-900/40 to-slate-900/40',
                    border: 'border-gray-500/40',
                    text: 'text-gray-400',
                    badge: 'bg-gray-500/20 text-gray-300 border-gray-500/30'
                };
        }
    };

    const getSeverityIcon = (severity) => {
        switch (severity?.toLowerCase()) {
            case 'high':
            case 'critical':
                return '🔴';
            case 'medium':
                return '🟡';
            case 'low':
                return '🟢';
            default:
                return '⚪';
        }
    };

    const riskCounts = {
        high: parsedRisks.filter(r => r.severity?.toLowerCase() === 'high' || r.severity?.toLowerCase() === 'critical').length,
        medium: parsedRisks.filter(r => r.severity?.toLowerCase() === 'medium').length,
        low: parsedRisks.filter(r => r.severity?.toLowerCase() === 'low').length
    };

    const totalRisks = parsedRisks.length;
    const riskScore = totalRisks === 0 ? 0 :
        ((riskCounts.high * 3 + riskCounts.medium * 2 + riskCounts.low * 1) / (totalRisks * 3) * 100);

    return (
        <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-gradient-to-br from-red-900/40 to-orange-900/40 backdrop-blur-md rounded-2xl p-6 border border-red-500/30 shadow-xl shadow-red-500/20 h-full flex flex-col"
        >
            {/* Header */}
            <div className="mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    <span className="text-3xl">⚠️</span>
                    Risk Factors
                </h2>
                <p className="text-red-300 text-sm mt-1">Identified Project Risks</p>
            </div>

            {/* Risk Score */}
            <div className="bg-white/10 rounded-xl p-4 border border-white/20 mb-4">
                <div className="text-center">
                    <div className="text-red-200 text-sm mb-2">Overall Risk Score</div>
                    <div className="text-5xl font-bold text-white mb-2">
                        {riskScore.toFixed(0)}
                    </div>
                    <div className="w-full bg-white/20 rounded-full h-2 overflow-hidden">
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${riskScore}%` }}
                            transition={{ duration: 1, ease: 'easeOut' }}
                            className={`h-full rounded-full ${riskScore >= 70 ? 'bg-red-500' :
                                    riskScore >= 40 ? 'bg-yellow-500' :
                                        'bg-green-500'
                                }`}
                        />
                    </div>
                </div>
            </div>

            {/* Risk Summary */}
            <div className="grid grid-cols-3 gap-2 mb-4">
                <div className="bg-red-500/10 rounded-lg p-2 border border-red-500/30 text-center">
                    <div className="text-red-400 font-bold text-xl">{riskCounts.high}</div>
                    <div className="text-red-300 text-xs">High</div>
                </div>
                <div className="bg-yellow-500/10 rounded-lg p-2 border border-yellow-500/30 text-center">
                    <div className="text-yellow-400 font-bold text-xl">{riskCounts.medium}</div>
                    <div className="text-yellow-300 text-xs">Medium</div>
                </div>
                <div className="bg-blue-500/10 rounded-lg p-2 border border-blue-500/30 text-center">
                    <div className="text-blue-400 font-bold text-xl">{riskCounts.low}</div>
                    <div className="text-blue-300 text-xs">Low</div>
                </div>
            </div>

            {/* Risks List */}
            <div className="space-y-3 flex-1 overflow-y-auto custom-scrollbar">
                {parsedRisks.length === 0 ? (
                    <div className="text-center py-8 text-green-300">
                        <div className="text-4xl mb-2">✅</div>
                        <div className="font-semibold">No risks identified</div>
                        <div className="text-sm text-green-400 mt-1">Project is on track!</div>
                    </div>
                ) : (
                    parsedRisks.map((risk, idx) => {
                        const colors = getSeverityColor(risk.severity);
                        return (
                            <motion.div
                                key={risk.id}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: idx * 0.1 }}
                                className={`bg-gradient-to-r ${colors.bg} backdrop-blur-sm rounded-xl p-4 border ${colors.border}`}
                            >
                                <div className="flex items-start gap-3">
                                    <div className="text-2xl flex-shrink-0">
                                        {getSeverityIcon(risk.severity)}
                                    </div>
                                    <div className="flex-1">
                                        <div className="flex items-start justify-between gap-2 mb-2">
                                            <h3 className="text-white font-semibold text-sm">
                                                {risk.factor}
                                            </h3>
                                            <span className={`text-xs px-2 py-1 rounded-full border ${colors.badge} capitalize whitespace-nowrap`}>
                                                {risk.severity || 'medium'}
                                            </span>
                                        </div>

                                        {risk.impact && (
                                            <div className="text-xs text-white/80 mb-2">
                                                <span className="font-semibold">Impact:</span> {risk.impact}
                                            </div>
                                        )}

                                        {risk.mitigation && (
                                            <div className="text-xs bg-white/10 rounded-lg p-2 border border-white/20">
                                                <span className="font-semibold text-green-300">💡 Mitigation:</span>
                                                <span className="text-white/90 ml-1">{risk.mitigation}</span>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </motion.div>
                        );
                    })
                )}
            </div>
        </motion.div>
    );
};

export default RiskFactorsCard;
