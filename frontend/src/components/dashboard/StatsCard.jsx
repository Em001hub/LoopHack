import React from 'react';
const StatsCard = ({ title, value }) => (
    <div className="bg-white rounded shadow p-4">
        <div className="text-gray-500">{title}</div>
        <div className="text-2xl font-bold">{value}</div>
    </div>
);
export default StatsCard;
