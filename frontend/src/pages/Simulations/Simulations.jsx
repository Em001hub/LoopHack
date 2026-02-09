import React from 'react';
import ScenarioBuilder from './ScenarioBuilder';
import TimelineComparison from './TimelineComparison';
import MonteCarloViz from './MonteCarloViz';

const Simulations = () => {
    return (
        <div>
            <h2>Simulations</h2>
            <ScenarioBuilder />
            <TimelineComparison />
            <MonteCarloViz />
        </div>
    );
};
export default Simulations;
