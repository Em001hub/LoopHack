/**
 * Data adapters to transform Intelligence Service API responses
 * to the format expected by the dashboard components
 */

/**
 * Transform team sentiment API response
 */
export const transformSentimentData = (apiData) => {
    if (!apiData) return null;

    return {
        overall_sentiment: apiData.overall_sentiment || 'neutral',
        sentiment_score: apiData.morale_score || 0,
        members_analyzed: apiData.members_analyzed || 0,
        positive_count: apiData.positive_count || 0,
        neutral_count: apiData.neutral_count || 0,
        negative_count: apiData.negative_count || 0,
        trends: {
            improving: apiData.trend === 'improving',
            change_percentage: apiData.trend_percentage || 0
        },
        insights: apiData.recommendations || []
    };
};

/**
 * Transform timeline prediction API response
 */
export const transformPredictionData = (apiData) => {
    if (!apiData) return null;

    return {
        predicted_completion_date: apiData.predicted_completion_date || apiData.predicted_date,
        predicted_weeks_remaining: apiData.predicted_weeks_remaining || apiData.weeks_remaining || 0,
        confidence_score: apiData.confidence_score || apiData.confidence || 0,
        probability_of_meeting_deadline: apiData.probability_of_meeting_deadline ||
            apiData.on_time_probability || 0,
        percentiles: {
            p10: apiData.percentiles?.p10 || 0,
            p25: apiData.percentiles?.p25 || 0,
            p50: apiData.percentiles?.p50 || apiData.predicted_weeks_remaining || 0,
            p75: apiData.percentiles?.p75 || 0,
            p90: apiData.percentiles?.p90 || 0
        },
        risk_factors: apiData.risk_factors || apiData.risks || [],
        recommendations: apiData.recommendations || []
    };
};

/**
 * Transform project insights API response
 */
export const transformInsightsData = (apiData) => {
    if (!apiData) return null;

    return {
        insights: apiData.insights || apiData.recommendations || [],
        categories: apiData.categories || {
            performance: 0,
            resources: 0,
            quality: 0,
            progress: 0
        },
        confidence_scores: apiData.confidence_scores || [],
        action_required: apiData.action_required || apiData.actions || []
    };
};

/**
 * Transform Monte Carlo simulation API response
 */
export const transformSimulationData = (apiData) => {
    if (!apiData) return null;

    return {
        simulation_count: apiData.simulation_count || apiData.n_simulations || 1000,
        predicted_weeks: {
            mean: apiData.predicted_weeks?.mean || apiData.mean_weeks || 0,
            median: apiData.predicted_weeks?.median || apiData.median_weeks || 0,
            std: apiData.predicted_weeks?.std || apiData.std_dev || 0,
            min: apiData.predicted_weeks?.min || apiData.min_weeks || 0,
            max: apiData.predicted_weeks?.max || apiData.max_weeks || 0
        },
        percentiles: {
            p10: apiData.percentiles?.p10 || 0,
            p25: apiData.percentiles?.p25 || 0,
            p50: apiData.percentiles?.p50 || 0,
            p75: apiData.percentiles?.p75 || 0,
            p90: apiData.percentiles?.p90 || 0
        },
        distribution: {
            bins: apiData.distribution?.bins || [],
            counts: apiData.distribution?.counts || []
        },
        recommendation: apiData.recommendation || apiData.recommendations?.[0] || ''
    };
};

export default {
    transformSentimentData,
    transformPredictionData,
    transformInsightsData,
    transformSimulationData
};
