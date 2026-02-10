import { motion } from 'framer-motion';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const SentimentAnalysisCard = ({ data, loading }) => {
    if (loading) {
        return (
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 h-full">
                <div className="animate-pulse">
                    <div className="h-8 bg-white/20 rounded w-2/3 mb-4"></div>
                    <div className="h-48 bg-white/20 rounded-full mx-auto w-48"></div>
                </div>
            </div>
        );
    }

    // Default data if none provided
    const sentimentData = data || {
        overall_sentiment: 'positive',
        sentiment_score: 0.75,
        members_analyzed: 8,
        positive_count: 6,
        neutral_count: 1,
        negative_count: 1,
        trends: {
            improving: true,
            change_percentage: 12
        }
    };

    const {
        overall_sentiment,
        sentiment_score = 0.75,
        members_analyzed = 0,
        positive_count = 0,
        neutral_count = 0,
        negative_count = 0,
        trends = {}
    } = sentimentData;

    // Chart data
    const chartData = {
        labels: ['Positive', 'Neutral', 'Negative'],
        datasets: [
            {
                data: [positive_count, neutral_count, negative_count],
                backgroundColor: [
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(234, 179, 8, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: [
                    'rgb(34, 197, 94)',
                    'rgb(234, 179, 8)',
                    'rgb(239, 68, 68)'
                ],
                borderWidth: 2
            }
        ]
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: 'rgba(255, 255, 255, 0.8)',
                    padding: 15,
                    font: {
                        size: 12
                    }
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                padding: 12,
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: 'rgba(147, 51, 234, 0.5)',
                borderWidth: 1
            }
        }
    };

    const getSentimentEmoji = (sentiment) => {
        switch (sentiment?.toLowerCase()) {
            case 'positive':
                return '😊';
            case 'neutral':
                return '😐';
            case 'negative':
                return '😟';
            default:
                return '😊';
        }
    };

    const getSentimentColor = (sentiment) => {
        switch (sentiment?.toLowerCase()) {
            case 'positive':
                return 'text-green-400';
            case 'neutral':
                return 'text-yellow-400';
            case 'negative':
                return 'text-red-400';
            default:
                return 'text-green-400';
        }
    };

    const scorePercentage = (sentiment_score * 100).toFixed(0);

    return (
        <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-gradient-to-br from-green-900/40 to-emerald-900/40 backdrop-blur-md rounded-2xl p-6 border border-green-500/30 shadow-xl shadow-green-500/20 h-full flex flex-col"
        >
            {/* Header */}
            <div className="mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    <span className="text-3xl">{getSentimentEmoji(overall_sentiment)}</span>
                    Team Sentiment
                </h2>
                <p className="text-green-300 text-sm mt-1">Real-time Morale Analysis</p>
            </div>

            {/* Overall Sentiment */}
            <div className="bg-white/10 rounded-xl p-4 border border-white/20 mb-4">
                <div className="text-center">
                    <div className="text-green-200 text-sm mb-2">Overall Sentiment</div>
                    <div className={`text-4xl font-bold capitalize ${getSentimentColor(overall_sentiment)}`}>
                        {overall_sentiment || 'Positive'}
                    </div>
                    <div className="mt-2">
                        <div className="w-full bg-white/20 rounded-full h-3 overflow-hidden">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${scorePercentage}%` }}
                                transition={{ duration: 1, ease: 'easeOut' }}
                                className="bg-gradient-to-r from-green-500 to-emerald-400 h-full rounded-full"
                            />
                        </div>
                        <div className="text-white text-sm mt-1">{scorePercentage}% Positive</div>
                    </div>
                </div>
            </div>

            {/* Sentiment Distribution Chart */}
            <div className="bg-white/5 rounded-xl p-4 border border-white/10 mb-4 flex-1">
                <h3 className="text-white font-semibold mb-3 text-center">Distribution</h3>
                <div className="h-48">
                    <Doughnut data={chartData} options={chartOptions} />
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-3">
                <div className="bg-white/5 rounded-xl p-3 border border-white/10">
                    <div className="text-green-300 text-xs mb-1">Team Members</div>
                    <div className="text-white font-bold text-2xl">{members_analyzed}</div>
                </div>

                {trends.improving !== undefined && (
                    <div className="bg-white/5 rounded-xl p-3 border border-white/10">
                        <div className="text-green-300 text-xs mb-1">Trend</div>
                        <div className={`font-bold text-2xl ${trends.improving ? 'text-green-400' : 'text-red-400'}`}>
                            {trends.improving ? '↗' : '↘'} {Math.abs(trends.change_percentage || 0)}%
                        </div>
                    </div>
                )}
            </div>

            {/* Insights */}
            {sentimentData.insights && sentimentData.insights.length > 0 && (
                <div className="mt-4 bg-gradient-to-r from-blue-900/30 to-cyan-900/30 rounded-xl p-3 border border-blue-500/30">
                    <div className="text-blue-300 text-xs font-semibold mb-2">💬 Key Insights</div>
                    <ul className="space-y-1">
                        {sentimentData.insights.slice(0, 2).map((insight, idx) => (
                            <li key={idx} className="text-blue-100 text-xs flex items-start gap-1">
                                <span className="text-blue-400">•</span>
                                <span>{insight}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </motion.div>
    );
};

export default SentimentAnalysisCard;
