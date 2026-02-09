import { motion } from 'framer-motion';
import { Bar, Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const MonteCarloSimulation = ({ data, projectId }) => {
    if (!data) {
        return null;
    }

    const {
        simulation_count = 1000,
        predicted_weeks = {},
        percentiles = {},
        distribution = {},
        scenarios = []
    } = data;

    // Distribution histogram data
    const histogramData = {
        labels: distribution.bins?.map(bin => `${bin.toFixed(1)}w`) || [],
        datasets: [
            {
                label: 'Frequency',
                data: distribution.counts || [],
                backgroundColor: 'rgba(147, 51, 234, 0.6)',
                borderColor: 'rgb(147, 51, 234)',
                borderWidth: 2,
                borderRadius: 4
            }
        ]
    };

    const histogramOptions = {
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
                    label: (context) => `${context.parsed.y} simulations`
                }
            },
            title: {
                display: true,
                text: 'Distribution of Completion Times',
                color: 'rgba(255, 255, 255, 0.9)',
                font: {
                    size: 16,
                    weight: 'bold'
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
                    color: 'rgba(255, 255, 255, 0.7)'
                },
                title: {
                    display: true,
                    text: 'Frequency',
                    color: 'rgba(255, 255, 255, 0.7)'
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.7)'
                },
                title: {
                    display: true,
                    text: 'Weeks to Completion',
                    color: 'rgba(255, 255, 255, 0.7)'
                }
            }
        }
    };

    // Percentile comparison data
    const percentileData = {
        labels: ['P10', 'P25', 'P50', 'P75', 'P90'],
        datasets: [
            {
                label: 'Weeks',
                data: [
                    percentiles.p10 || 0,
                    percentiles.p25 || 0,
                    percentiles.p50 || 0,
                    percentiles.p75 || 0,
                    percentiles.p90 || 0
                ],
                borderColor: 'rgb(34, 197, 94)',
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 6,
                pointHoverRadius: 8,
                pointBackgroundColor: 'rgb(34, 197, 94)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }
        ]
    };

    const percentileOptions = {
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
                borderColor: 'rgba(34, 197, 94, 0.5)',
                borderWidth: 1,
                callbacks: {
                    label: (context) => `${context.parsed.y.toFixed(1)} weeks`
                }
            },
            title: {
                display: true,
                text: 'Confidence Intervals',
                color: 'rgba(255, 255, 255, 0.9)',
                font: {
                    size: 16,
                    weight: 'bold'
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

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-gradient-to-br from-indigo-900/40 to-purple-900/40 backdrop-blur-md rounded-2xl p-6 border border-indigo-500/30 shadow-xl shadow-indigo-500/20"
        >
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                        <span className="text-3xl">🎲</span>
                        Monte Carlo Simulation
                    </h2>
                    <p className="text-indigo-300 text-sm mt-1">
                        {simulation_count.toLocaleString()} simulations for {projectId}
                    </p>
                </div>

                <div className="bg-white/10 rounded-xl px-4 py-2 border border-white/20">
                    <div className="text-indigo-200 text-xs">Confidence Level</div>
                    <div className="text-white font-bold text-lg">95%</div>
                </div>
            </div>

            {/* Summary Statistics */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="text-indigo-300 text-sm mb-1">Mean</div>
                    <div className="text-white font-bold text-2xl">
                        {predicted_weeks.mean?.toFixed(1) || 'N/A'}
                    </div>
                    <div className="text-indigo-400 text-xs mt-1">weeks</div>
                </div>

                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="text-indigo-300 text-sm mb-1">Median</div>
                    <div className="text-cyan-400 font-bold text-2xl">
                        {predicted_weeks.median?.toFixed(1) || percentiles.p50?.toFixed(1) || 'N/A'}
                    </div>
                    <div className="text-indigo-400 text-xs mt-1">weeks</div>
                </div>

                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="text-indigo-300 text-sm mb-1">Std Dev</div>
                    <div className="text-yellow-400 font-bold text-2xl">
                        {predicted_weeks.std?.toFixed(1) || 'N/A'}
                    </div>
                    <div className="text-indigo-400 text-xs mt-1">weeks</div>
                </div>

                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="text-indigo-300 text-sm mb-1">Min</div>
                    <div className="text-green-400 font-bold text-2xl">
                        {predicted_weeks.min?.toFixed(1) || 'N/A'}
                    </div>
                    <div className="text-indigo-400 text-xs mt-1">weeks</div>
                </div>

                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="text-indigo-300 text-sm mb-1">Max</div>
                    <div className="text-red-400 font-bold text-2xl">
                        {predicted_weeks.max?.toFixed(1) || 'N/A'}
                    </div>
                    <div className="text-indigo-400 text-xs mt-1">weeks</div>
                </div>
            </div>

            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Distribution Histogram */}
                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="h-80">
                        <Bar data={histogramData} options={histogramOptions} />
                    </div>
                </div>

                {/* Percentile Chart */}
                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="h-80">
                        <Line data={percentileData} options={percentileOptions} />
                    </div>
                </div>
            </div>

            {/* Percentile Table */}
            <div className="mt-6 bg-white/5 rounded-xl p-4 border border-white/10">
                <h3 className="text-white font-semibold mb-3">Percentile Breakdown</h3>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                    {[
                        { label: '10th', key: 'p10', desc: 'Best case' },
                        { label: '25th', key: 'p25', desc: 'Optimistic' },
                        { label: '50th', key: 'p50', desc: 'Most likely' },
                        { label: '75th', key: 'p75', desc: 'Conservative' },
                        { label: '90th', key: 'p90', desc: 'Worst case' }
                    ].map(({ label, key, desc }) => (
                        <div key={key} className="bg-white/5 rounded-lg p-3 border border-white/10">
                            <div className="text-indigo-300 text-xs mb-1">{label} Percentile</div>
                            <div className="text-white font-bold text-xl">
                                {percentiles[key]?.toFixed(1) || 'N/A'}w
                            </div>
                            <div className="text-indigo-400 text-xs mt-1">{desc}</div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Recommendation */}
            {data.recommendation && (
                <div className="mt-6 bg-gradient-to-r from-green-900/30 to-emerald-900/30 rounded-xl p-4 border border-green-500/30">
                    <h3 className="text-green-300 font-semibold mb-2 flex items-center gap-2">
                        <span>💡</span>
                        Recommendation
                    </h3>
                    <p className="text-green-100 text-sm">{data.recommendation}</p>
                </div>
            )}
        </motion.div>
    );
};

export default MonteCarloSimulation;
