import { motion } from 'framer-motion';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';
import { format, differenceInDays } from 'date-fns';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const TimelinePredictionCard = ({ data, loading, projectId }) => {
    if (loading) {
        return (
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 h-full">
                <div className="animate-pulse">
                    <div className="h-8 bg-white/20 rounded w-1/3 mb-4"></div>
                    <div className="h-64 bg-white/20 rounded"></div>
                </div>
            </div>
        );
    }

    if (!data) {
        return (
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 h-full flex items-center justify-center">
                <p className="text-purple-300">No prediction data available</p>
            </div>
        );
    }

    const predictedDate = data.predicted_completion_date ? new Date(data.predicted_completion_date) : null;
    const daysRemaining = predictedDate ? differenceInDays(predictedDate, new Date()) : 0;
    const weeksRemaining = data.predicted_weeks_remaining || 0;

    // Chart data for confidence intervals
    const chartData = {
        labels: ['P10', 'P25', 'P50 (Median)', 'P75', 'P90'],
        datasets: [
            {
                label: 'Weeks to Completion',
                data: [
                    data.percentiles?.p10 || 0,
                    data.percentiles?.p25 || 0,
                    data.percentiles?.p50 || weeksRemaining,
                    data.percentiles?.p75 || 0,
                    data.percentiles?.p90 || 0
                ],
                borderColor: 'rgb(147, 51, 234)',
                backgroundColor: 'rgba(147, 51, 234, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 6,
                pointHoverRadius: 8,
                pointBackgroundColor: 'rgb(147, 51, 234)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }
        ]
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                padding: 12,
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: 'rgba(147, 51, 234, 0.5)',
                borderWidth: 1,
                callbacks: {
                    label: (context) => `${context.parsed.y.toFixed(1)} weeks`
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.7)',
                    callback: (value) => `${value}w`
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.7)'
                }
            }
        }
    };

    const probabilityOfSuccess = data.probability_of_meeting_deadline || 0;
    const probabilityColor = probabilityOfSuccess >= 70 ? 'text-green-400' :
        probabilityOfSuccess >= 40 ? 'text-yellow-400' : 'text-red-400';

    return (
        <motion.div
            whileHover={{ scale: 1.01 }}
            className="bg-gradient-to-br from-purple-900/40 to-pink-900/40 backdrop-blur-md rounded-2xl p-6 border border-purple-500/30 shadow-xl shadow-purple-500/20 h-full"
        >
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                        <span className="text-3xl">📊</span>
                        Timeline Prediction
                    </h2>
                    <p className="text-purple-300 text-sm mt-1">ML-Powered Completion Forecast</p>
                </div>

                {data.confidence_score && (
                    <div className="bg-white/10 rounded-xl px-4 py-2 border border-white/20">
                        <div className="text-purple-200 text-xs">Confidence</div>
                        <div className="text-white font-bold text-lg">
                            {(data.confidence_score * 100).toFixed(0)}%
                        </div>
                    </div>
                )}
            </div>

            {/* Main Stats */}
            <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="text-purple-300 text-sm mb-1">Predicted Completion</div>
                    <div className="text-white font-bold text-xl">
                        {predictedDate ? format(predictedDate, 'MMM dd, yyyy') : 'N/A'}
                    </div>
                    <div className="text-purple-400 text-sm mt-1">
                        {daysRemaining > 0 ? `${daysRemaining} days` : 'Overdue'}
                    </div>
                </div>

                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="text-purple-300 text-sm mb-1">Weeks Remaining</div>
                    <div className="text-cyan-400 font-bold text-3xl">
                        {weeksRemaining.toFixed(1)}
                    </div>
                    <div className="text-purple-400 text-sm mt-1">weeks</div>
                </div>

                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="text-purple-300 text-sm mb-1">Success Probability</div>
                    <div className={`font-bold text-3xl ${probabilityColor}`}>
                        {probabilityOfSuccess.toFixed(0)}%
                    </div>
                    <div className="text-purple-400 text-sm mt-1">on-time delivery</div>
                </div>
            </div>

            {/* Confidence Interval Chart */}
            <div className="bg-white/5 rounded-xl p-4 border border-white/10 mb-4">
                <h3 className="text-white font-semibold mb-3">Confidence Intervals</h3>
                <div className="h-48">
                    <Line data={chartData} options={chartOptions} />
                </div>
            </div>

            {/* Recommendations */}
            {data.recommendations && data.recommendations.length > 0 && (
                <div className="bg-gradient-to-r from-green-900/30 to-emerald-900/30 rounded-xl p-4 border border-green-500/30">
                    <h3 className="text-green-300 font-semibold mb-2 flex items-center gap-2">
                        <span>💡</span>
                        Recommendations
                    </h3>
                    <ul className="space-y-2">
                        {data.recommendations.slice(0, 3).map((rec, idx) => (
                            <li key={idx} className="text-green-100 text-sm flex items-start gap-2">
                                <span className="text-green-400 mt-1">•</span>
                                <span>{rec}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </motion.div>
    );
};

export default TimelinePredictionCard;
