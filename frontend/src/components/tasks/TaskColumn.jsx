import React from 'react';
import TaskCard from './TaskCard';

const TaskColumn = ({ title, tasks }) => (
    <div className="w-1/3 bg-gray-100 p-4 rounded mr-4">
        <h3 className="font-bold mb-4">{title}</h3>
        {tasks.map(task => <TaskCard key={task.id} task={task} />)}
    </div>
);
export default TaskColumn;
