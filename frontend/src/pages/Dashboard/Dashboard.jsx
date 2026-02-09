import React from 'react';
import QuickStats from './QuickStats';
import ProjectCard from './ProjectCard';
import NeedsAttention from './NeedsAttention';

const Dashboard = () => {
    return (
        <div>
            <h3 className="text-gray-700 text-3xl font-medium">Dashboard</h3>
            <QuickStats />
            <div className="mt-8">
                <NeedsAttention />
            </div>
            <div className="flex flex-wrap -mx-6 mt-8">
                <div className="w-full px-6 sm:w-1/2 xl:w-1/3">
                    <ProjectCard />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
