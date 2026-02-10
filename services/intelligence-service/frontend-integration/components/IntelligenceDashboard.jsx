import React, { useState, useEffect } from 'react';
import {
    usePredictions,
    useSkills,
    useSentiment,
    useInsights
} from '../react-hooks/useIntelligence';

/**
 * Intelligence Dashboard Component
 * 
 * Displays comprehensive project intelligence including:
 * - Timeline predictions with confidence intervals
 * - Team sentiment analysis
 * - Skill matrix visualization
 * - AI-generated insights and recommendations
 */
const IntelligenceDashboard = ({ projectId }) => {
    const [activeTab, setActiveTab] = useState('overview');
    const [refreshInterval, setRefreshInterval] = useState(30000); // 30 seconds

    // Fetch data using custom hooks
    const {
        prediction,
        loading: predictionLoading,
        error: predictionError,
        refresh: refreshPrediction
    } = usePredictions(projectId);

    const {
        teamMorale,
        loading: sentimentLoading,
        refresh: refreshSentiment
    } = useSentiment(projectId);

    const {
        insights,
        loading: insightsLoading,
        refresh: refreshInsights
    } = useInsights(projectId);

    // Auto-refresh
    useEffect(() => {
        const interval = setInterval(() => {
            refreshPrediction();
            refreshSentiment();
            refreshInsights();
        }, refreshInterval);

        return () => clearInterval(interval);
    }, [refreshInterval, refreshPrediction, refreshSentiment, refreshInsights]);

    // Loading state
    if (predictionLoading || sentimentLoading || insightsLoading) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-50">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600 text-lg">Loading intelligence data...</p>
                </div>
            </div>
        );
    }

    // Error state
    if (predictionError) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-50">
                <div className="bg-red-50 border border-red-200 rounded-lg p-8 max-w-md">
                    <div className="flex items-center mb-4">
                        <svg className="w-6 h-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <h3 className="text-red-800 font-semibold text-lg">Error Loading Data</h3>
                    </div>
                    <p className="text-red-700 mb-4">{predictionError}</p>
                    <button
                        onClick={() => window.location.reload()}
                        className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
                    >
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-2">
                                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                </svg>
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-gray-900">Intelligence Dashboard</h1>
                                <p className="text-sm text-gray-500">Project: {projectId}</p>
                            </div>
                        </div>
                        <div className="flex items-center space-x-3">
                            <span className="text-sm text-gray-500">Auto-refresh: {refreshInterval / 1000}s</span>
                            <button
                                onClick={() => {
                                    refreshPrediction();
                                    refreshSentiment();
                                    refreshInsights();
                                }}
                                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition flex items-center space-x-2"
                            >
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                </svg>
                                <span>Refresh</span>
                            </button>
                        </div>
                    </div>
                </div>

                {/* Tabs */}
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <nav className="flex space-x-8" aria-label="Tabs">
                        {['overview', 'timeline', 'sentiment', 'insights'].map((tab) => (
                            <button
                                key={tab}
                                onClick={() => setActiveTab(tab)}
                                className={`py-4 px-1 border-b-2 font-medium text-sm transition ${activeTab === tab
                                        ? 'border-blue-600 text-blue-600'
                                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                    }`}
                            >
                                {tab.charAt(0).toUpperCase() + tab.slice(1)}
                            </button>
                        ))}
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {activeTab === 'overview' && (
                    <OverviewTab
                        prediction={prediction}
                        teamMorale={teamMorale}
                        insights={insights}
                    />
                )}
                {activeTab === 'timeline' && <TimelineTab prediction={prediction} />}
                {activeTab === 'sentiment' && <SentimentTab teamMorale={teamMorale} />}
                {activeTab === 'insights' && <InsightsTab insights={insights} />}
            </main>
        </div>
    );
};

/**
 * Overview Tab Component
 */
const OverviewTab = ({ prediction, teamMorale, insights }) => {
    return (
        <div className="space-y-6">
            {/* Key Metrics Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Timeline Prediction Card */}
                <MetricCard
                    title="Predicted Completion"
                    value={new Date(prediction?.predicted_completion_date).toLocaleDateString()}
                    subtitle={`${prediction?.predicted_weeks_remaining?.toFixed(1)} weeks remaining`}
                    icon={
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                    }
                    color="blue"
                    confidence={prediction?.model_confidence}
                />

                {/* On-Time Probability Card */}
                <MetricCard
                    title="On-Time Probability"
                    value={`${(prediction?.probability_on_time * 100)?.toFixed(0) || 0}%`}
                    subtitle={prediction?.probability_on_time > 0.7 ? "High confidence" : "At risk"}
                    icon={
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    }
                    color={prediction?.probability_on_time > 0.7 ? "green" : "yellow"}
                />

                {/* Team Morale Card */}
                <MetricCard
                    title="Team Morale"
                    value={teamMorale?.team_morale?.label || "N/A"}
                    subtitle={`${teamMorale?.members_analyzed || 0} members analyzed`}
                    icon={
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    }
                    color={getSentimentColor(teamMorale?.team_morale?.label)}
                />
            </div>

            {/* Timeline Confidence Interval */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Timeline Confidence Intervals</h3>
                <ConfidenceIntervalChart prediction={prediction} />
            </div>

            {/* Risk Factors */}
            {prediction?.risk_factors && prediction.risk_factors.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center mb-4">
                        <svg className="w-5 h-5 text-yellow-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        <h3 className="text-lg font-semibold text-gray-900">Risk Factors</h3>
                    </div>
                    <ul className="space-y-2">
                        {prediction.risk_factors.map((risk, index) => (
                            <li key={index} className="flex items-start">
                                <span className="text-yellow-600 mr-2">•</span>
                                <span className="text-gray-700">{risk}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* At-Risk Team Members */}
            {teamMorale?.at_risk_members && teamMorale.at_risk_members.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center mb-4">
                        <svg className="w-5 h-5 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        <h3 className="text-lg font-semibold text-gray-900">At-Risk Team Members</h3>
                    </div>
                    <div className="space-y-3">
                        {teamMorale.at_risk_members.map((member, index) => (
                            <div key={index} className="bg-red-50 border border-red-200 rounded-lg p-4">
                                <div className="flex items-center justify-between mb-2">
                                    <span className="font-medium text-gray-900">{member.user_id}</span>
                                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${member.risk_level === 'High'
                                            ? 'bg-red-600 text-white'
                                            : 'bg-yellow-600 text-white'
                                        }`}>
                                        {member.risk_level} Risk
                                    </span>
                                </div>
                                <p className="text-sm text-gray-600 mb-2">Score: {member.risk_score}/100</p>
                                <p className="text-sm text-gray-700 font-medium">
                                    Action: {member.recommended_action}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Top Insights */}
            {insights?.highlights && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Today's Highlights</h3>
                    <ul className="space-y-2">
                        {insights.highlights.map((highlight, index) => (
                            <li key={index} className="flex items-start">
                                <span className="text-blue-600 mr-2">•</span>
                                <span className="text-gray-700">{highlight}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

/**
 * Timeline Tab Component
 */
const TimelineTab = ({ prediction }) => {
    return (
        <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6">Timeline Analysis</h2>

                {/* Prediction Summary */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                    <div>
                        <h3 className="text-sm font-medium text-gray-500 mb-2">Predicted Completion</h3>
                        <p className="text-3xl font-bold text-gray-900">
                            {new Date(prediction?.predicted_completion_date).toLocaleDateString('en-US', {
                                weekday: 'long',
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric'
                            })}
                        </p>
                        <p className="text-sm text-gray-600 mt-2">
                            {prediction?.predicted_weeks_remaining?.toFixed(1)} weeks remaining
                        </p>
                    </div>
                    <div>
                        <h3 className="text-sm font-medium text-gray-500 mb-2">Confidence</h3>
                        <div className="flex items-center space-x-4">
                            <div className="flex-1">
                                <div className="w-full bg-gray-200 rounded-full h-3">
                                    <div
                                        className="bg-blue-600 h-3 rounded-full transition-all duration-500"
                                        style={{ width: `${(prediction?.model_confidence * 100)}%` }}
                                    ></div>
                                </div>
                            </div>
                            <span className="text-2xl font-bold text-gray-900">
                                {(prediction?.model_confidence * 100)?.toFixed(0)}%
                            </span>
                        </div>
                    </div>
                </div>

                {/* Confidence Intervals */}
                <div className="mb-8">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Confidence Intervals</h3>
                    <ConfidenceIntervalChart prediction={prediction} />
                </div>

                {/* Risk Breakdown */}
                <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Factors</h3>
                    {prediction?.risk_factors && prediction.risk_factors.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {prediction.risk_factors.map((risk, index) => (
                                <div key={index} className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                                    <div className="flex items-start">
                                        <svg className="w-5 h-5 text-yellow-600 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                        </svg>
                                        <span className="text-gray-700">{risk}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-gray-500">No significant risk factors detected</p>
                    )}
                </div>
            </div>
        </div>
    );
};

/**
 * Sentiment Tab Component
 */
const SentimentTab = ({ teamMorale }) => {
    return (
        <div className="space-y-6">
            {/* Team Overview */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6">Team Sentiment Overview</h2>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div className="text-center">
                        <div className={`inline-flex items-center justify-center w-20 h-20 rounded-full mb-3 ${getSentimentBgColor(teamMorale?.team_morale?.label)
                            }`}>
                            {getSentimentIcon(teamMorale?.team_morale?.label)}
                        </div>
                        <h3 className="text-sm font-medium text-gray-500 mb-1">Overall Morale</h3>
                        <p className="text-2xl font-bold text-gray-900">{teamMorale?.team_morale?.label || 'N/A'}</p>
                        <p className="text-sm text-gray-600 mt-1">
                            Score: {teamMorale?.team_morale?.average_sentiment?.toFixed(2) || 'N/A'}
                        </p>
                    </div>
                    <div className="text-center">
                        <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-green-100 mb-3">
                            <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <h3 className="text-sm font-medium text-gray-500 mb-1">High Morale</h3>
                        <p className="text-2xl font-bold text-green-600">{teamMorale?.high_morale_count || 0}</p>
                        <p className="text-sm text-gray-600 mt-1">team members</p>
                    </div>
                    <div className="text-center">
                        <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-red-100 mb-3">
                            <svg className="w-10 h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <h3 className="text-sm font-medium text-gray-500 mb-1">At Risk</h3>
                        <p className="text-2xl font-bold text-red-600">{teamMorale?.at_risk_members?.length || 0}</p>
                        <p className="text-sm text-gray-600 mt-1">team members</p>
                    </div>
                </div>

                {/* Trend Indicator */}
                <div className="flex items-center justify-center p-4 bg-gray-50 rounded-lg">
                    <span className="text-sm text-gray-600 mr-2">Trend:</span>
                    <span className={`font-semibold flex items-center ${teamMorale?.team_morale?.trend === 'improving' ? 'text-green-600' :
                            teamMorale?.team_morale?.trend === 'declining' ? 'text-red-600' :
                                'text-gray-600'
                        }`}>
                        {teamMorale?.team_morale?.trend === 'improving' && (
                            <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                            </svg>
                        )}
                        {teamMorale?.team_morale?.trend === 'declining' && (
                            <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                            </svg>
                        )}
                        {teamMorale?.team_morale?.trend || 'Stable'}
                    </span>
                </div>
            </div>

            {/* At-Risk Members Details */}
            {teamMorale?.at_risk_members && teamMorale.at_risk_members.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">At-Risk Team Members</h3>
                    <div className="space-y-4">
                        {teamMorale.at_risk_members.map((member, index) => (
                            <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                                <div className="flex items-center justify-between mb-3">
                                    <div className="flex items-center">
                                        <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center mr-3">
                                            <span className="text-gray-600 font-semibold">
                                                {member.user_id?.charAt(0)?.toUpperCase()}
                                            </span>
                                        </div>
                                        <div>
                                            <h4 className="font-semibold text-gray-900">{member.user_id}</h4>
                                            <p className="text-sm text-gray-500">Burnout Risk: {member.risk_level}</p>
                                        </div>
                                    </div>
                                    <span className={`px-4 py-2 rounded-full text-sm font-semibold ${member.risk_level === 'High'
                                            ? 'bg-red-100 text-red-800'
                                            : 'bg-yellow-100 text-yellow-800'
                                        }`}>
                                        Score: {member.risk_score}/100
                                    </span>
                                </div>
                                <div className="bg-gray-50 rounded p-3">
                                    <p className="text-sm font-medium text-gray-700 mb-1">Recommended Action:</p>
                                    <p className="text-sm text-gray-600">{member.recommended_action}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Team Members Summary */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">All Team Members</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {Object.entries(teamMorale?.member_details || {}).map(([userId, details]) => (
                        <div key={userId} className="border border-gray-200 rounded-lg p-4">
                            <div className="flex items-center mb-2">
                                <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center mr-2">
                                    <span className="text-gray-600 font-semibold text-sm">
                                        {userId?.charAt(0)?.toUpperCase()}
                                    </span>
                                </div>
                                <span className="font-medium text-gray-900 text-sm">{userId}</span>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-xs text-gray-500">Sentiment:</span>
                                <span className={`px-2 py-1 rounded text-xs font-semibold ${getSentimentBadgeColor(details?.current_sentiment?.label)
                                    }`}>
                                    {details?.current_sentiment?.label || 'N/A'}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

/**
 * Insights Tab Component
 */
const InsightsTab = ({ insights }) => {
    return (
        <div className="space-y-6">
            {/* Summary */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-lg p-6 text-white">
                <h2 className="text-2xl font-bold mb-3">AI-Generated Insights</h2>
                <p className="text-blue-100">{insights?.summary || 'Analyzing project data...'}</p>
                <p className="text-sm text-blue-200 mt-2">Generated: {insights?.date || new Date().toLocaleDateString()}</p>
            </div>

            {/* Highlights */}
            {insights?.highlights && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center mb-4">
                        <svg className="w-6 h-6 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <h3 className="text-lg font-semibold text-gray-900">Highlights</h3>
                    </div>
                    <ul className="space-y-3">
                        {insights.highlights.map((highlight, index) => (
                            <li key={index} className="flex items-start bg-green-50 rounded-lg p-3">
                                <span className="text-green-600 mr-2">✓</span>
                                <span className="text-gray-700">{highlight}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Risks */}
            {insights?.risks && insights.risks.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center mb-4">
                        <svg className="w-6 h-6 text-yellow-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        <h3 className="text-lg font-semibold text-gray-900">Risks & Actions</h3>
                    </div>
                    <div className="space-y-4">
                        {insights.risks.map((risk, index) => (
                            <div key={index} className="border border-yellow-200 bg-yellow-50 rounded-lg p-4">
                                <div className="flex items-start justify-between mb-2">
                                    <div className="flex-1">
                                        <div className="flex items-center mb-1">
                                            <span className={`px-2 py-1 rounded text-xs font-semibold mr-2 ${risk.severity === 'high' ? 'bg-red-100 text-red-800' :
                                                    risk.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                                        'bg-blue-100 text-blue-800'
                                                }`}>
                                                {risk.severity?.toUpperCase()}
                                            </span>
                                            <span className="text-xs text-gray-500">{risk.type}</span>
                                        </div>
                                        <p className="text-gray-900 font-medium">{risk.description}</p>
                                    </div>
                                </div>
                                <div className="bg-white rounded p-3 mt-3">
                                    <p className="text-sm font-medium text-gray-700 mb-1">Recommended Action:</p>
                                    <p className="text-sm text-gray-600">{risk.recommended_action}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Opportunities */}
            {insights?.opportunities && insights.opportunities.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center mb-4">
                        <svg className="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        <h3 className="text-lg font-semibold text-gray-900">Opportunities</h3>
                    </div>
                    <ul className="space-y-3">
                        {insights.opportunities.map((opportunity, index) => (
                            <li key={index} className="flex items-start bg-blue-50 rounded-lg p-3">
                                <span className="text-blue-600 mr-2">→</span>
                                <span className="text-gray-700">{opportunity}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Predictions */}
            {insights?.predictions && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center mb-4">
                        <svg className="w-6 h-6 text-purple-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        <h3 className="text-lg font-semibold text-gray-900">AI Predictions</h3>
                    </div>
                    <div className="space-y-3">
                        {Object.entries(insights.predictions).map(([key, value]) => (
                            <div key={key} className="bg-purple-50 rounded-lg p-4">
                                <p className="text-sm font-medium text-purple-900 mb-1">
                                    {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                                </p>
                                <p className="text-gray-700">{value}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

/**
 * Metric Card Component
 */
const MetricCard = ({ title, value, subtitle, icon, color, confidence }) => {
    const colorClasses = {
        blue: 'bg-blue-100 text-blue-600',
        green: 'bg-green-100 text-green-600',
        yellow: 'bg-yellow-100 text-yellow-600',
        red: 'bg-red-100 text-red-600',
        purple: 'bg-purple-100 text-purple-600'
    };

    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition">
            <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-lg ${colorClasses[color] || colorClasses.blue}`}>
                    {icon}
                </div>
                {confidence && (
                    <span className="text-xs text-gray-500">
                        {(confidence * 100).toFixed(0)}% confidence
                    </span>
                )}
            </div>
            <h3 className="text-sm font-medium text-gray-500 mb-1">{title}</h3>
            <p className="text-2xl font-bold text-gray-900 mb-1">{value}</p>
            <p className="text-sm text-gray-600">{subtitle}</p>
        </div>
    );
};

/**
 * Confidence Interval Chart Component
 */
const ConfidenceIntervalChart = ({ prediction }) => {
    if (!prediction?.confidence_intervals) return null;

    const p10Date = new Date(prediction.confidence_intervals.p10);
    const p50Date = new Date(prediction.confidence_intervals.p50);
    const p90Date = new Date(prediction.confidence_intervals.p90);

    const today = new Date();
    const totalDays = (p90Date - today) / (1000 * 60 * 60 * 24);
    const p10Position = ((p10Date - today) / (1000 * 60 * 60 * 24) / totalDays) * 100;
    const p50Position = ((p50Date - today) / (1000 * 60 * 60 * 24) / totalDays) * 100;
    const p90Position = 100;

    return (
        <div className="relative">
            {/* Timeline Bar */}
            <div className="relative h-12 bg-gradient-to-r from-green-200 via-yellow-200 to-red-200 rounded-lg">
                {/* P10 Marker */}
                <div
                    className="absolute top-0 bottom-0 w-1 bg-green-600"
                    style={{ left: `${p10Position}%` }}
                >
                    <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-xs font-medium text-green-700 whitespace-nowrap">
                        10% (Best Case)
                    </div>
                </div>

                {/* P50 Marker */}
                <div
                    className="absolute top-0 bottom-0 w-1 bg-blue-600"
                    style={{ left: `${p50Position}%` }}
                >
                    <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-xs font-medium text-blue-700 whitespace-nowrap">
                        50% (Most Likely)
                    </div>
                </div>

                {/* P90 Marker */}
                <div
                    className="absolute top-0 bottom-0 w-1 bg-red-600"
                    style={{ left: `${p90Position}%` }}
                >
                    <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-xs font-medium text-red-700 whitespace-nowrap">
                        90% (Worst Case)
                    </div>
                </div>
            </div>

            {/* Date Labels */}
            <div className="flex justify-between mt-10 text-sm text-gray-600">
                <div className="text-center">
                    <p className="font-semibold">{p10Date.toLocaleDateString()}</p>
                    <p className="text-xs text-gray-500">Optimistic</p>
                </div>
                <div className="text-center">
                    <p className="font-semibold">{p50Date.toLocaleDateString()}</p>
                    <p className="text-xs text-gray-500">Expected</p>
                </div>
                <div className="text-center">
                    <p className="font-semibold">{p90Date.toLocaleDateString()}</p>
                    <p className="text-xs text-gray-500">Conservative</p>
                </div>
            </div>
        </div>
    );
};

/**
 * Helper Functions
 */
const getSentimentColor = (label) => {
    switch (label?.toLowerCase()) {
        case 'positive':
            return 'green';
        case 'negative':
            return 'red';
        default:
            return 'yellow';
    }
};

const getSentimentBgColor = (label) => {
    switch (label?.toLowerCase()) {
        case 'positive':
            return 'bg-green-100';
        case 'negative':
            return 'bg-red-100';
        default:
            return 'bg-yellow-100';
    }
};

const getSentimentBadgeColor = (label) => {
    switch (label?.toLowerCase()) {
        case 'positive':
            return 'bg-green-100 text-green-800';
        case 'negative':
            return 'bg-red-100 text-red-800';
        default:
            return 'bg-yellow-100 text-yellow-800';
    }
};

const getSentimentIcon = (label) => {
    switch (label?.toLowerCase()) {
        case 'positive':
            return (
                <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            );
        case 'negative':
            return (
                <svg className="w-10 h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            );
        default:
            return (
                <svg className="w-10 h-10 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            );
    }
};

export default IntelligenceDashboard;
