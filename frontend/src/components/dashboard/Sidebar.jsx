import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
    return (
        <div className="w-64 bg-gray-800 text-white h-full">
            <div className="p-4 text-2xl font-bold">LoopHack</div>
            <ul>
                <li className="p-4 hover:bg-gray-700"><Link to="/">Dashboard</Link></li>
                <li className="p-4 hover:bg-gray-700"><Link to="/projects">Projects</Link></li>
                <li className="p-4 hover:bg-gray-700"><Link to="/team">Team</Link></li>
                <li className="p-4 hover:bg-gray-700"><Link to="/chat">AI Chat</Link></li>
                <li className="p-4 hover:bg-gray-700"><Link to="/settings">Settings</Link></li>
            </ul>
        </div>
    );
};
export default Sidebar;
