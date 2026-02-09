import React from 'react';
const Modal = ({ isOpen, children }) => (
    isOpen ? <div className="fixed inset-0 bg-black bg-opacity-50">{children}</div> : null
);
export default Modal;
