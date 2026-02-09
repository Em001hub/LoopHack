import React from 'react';
import TaskColumn from './TaskColumn';

const KanbanBoard = ({ tasks }) => (
    <div className="flex">
        <TaskColumn title="To Do" tasks={tasks.filter(t => t.status === 'todo')} />
        <TaskColumn title="In Progress" tasks={tasks.filter(t => t.status === 'inprogress')} />
        <TaskColumn title="Done" tasks={tasks.filter(t => t.status === 'done')} />
    </div>
);
export default KanbanBoard;
