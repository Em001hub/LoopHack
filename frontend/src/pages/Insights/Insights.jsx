import React from 'react';
import PredictiveAlerts from './PredictiveAlerts';
import Recommendations from './Recommendations';

const Insights = () => {
    return (
        <div>
            <h2>AI Insights</h2>
            <PredictiveAlerts />
            <Recommendations />
        </div>
    );
};
export default Insights;
