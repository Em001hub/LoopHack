import { render, screen } from '@testing-library/react';
import TaskCard from '../components/tasks/TaskCard';

test('renders task title', () => {
    const task = { title: 'Test Task' };
    render(<TaskCard task={task} />);
    const linkElement = screen.getByText(/Test Task/i);
    expect(linkElement).toBeInTheDocument();
});
