import React from 'react';
const Badge = ({ text, color }) => <span className={`bg-${color}-100 text-${color}-800 px-2 py-1 rounded text-xs`}>{text}</span>;
export default Badge;
