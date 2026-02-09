import React from 'react';
const Button = ({ children, onClick, variant = 'primary' }) => (
    <button onClick={onClick} className={`btn btn-${variant}`}>{children}</button>
);
export default Button;
