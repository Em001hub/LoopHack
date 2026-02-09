import React from 'react';
import Timeline from './Timeline';
import TaskList from './TaskList';
import HealthMetrics from './HealthMetrics';
import ActivityFeed from './ActivityFeed';

const ProjectDetail = () => {
    return (
        <div>
            <h2>Project Alpha</h2>
            <Timeline />
            <div className="grid grid-cols-2 gap-4">
                <TaskList />
                <HealthMetrics />
            </div>
            <ActivityFeed />
        </div>
    );
};
export default ProjectDetail;
