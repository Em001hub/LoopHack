import { render, screen } from '@testing-library/react';
import Dashboard from '../pages/Dashboard/Dashboard';

test('renders dashboard heading', () => {
    render(<Dashboard />);
    const linkElement = screen.getByText(/Dashboard/i);
    expect(linkElement).toBeInTheDocument();
});
