import React from 'react';
import WorkloadHeatmap from './WorkloadHeatmap';
import SkillsMatrix from './SkillsMatrix';
import CollaborationGraph from './CollaborationGraph';
import MemberCard from './MemberCard';

const TeamAnalytics = () => {
    return (
        <div>
            <h2>Team Analytics</h2>
            <div className="grid grid-cols-2 gap-4">
                <WorkloadHeatmap />
                <SkillsMatrix />
            </div>
            <CollaborationGraph />
            <div className="mt-4">
                <MemberCard name="Alice" />
                <MemberCard name="Bob" />
            </div>
        </div>
    );
};
export default TeamAnalytics;
