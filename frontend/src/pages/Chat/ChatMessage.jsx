import React from 'react';
const ChatMessage = ({ text, isUser }) => (
    <div className={`p-2 rounded ${isUser ? 'bg-blue-100 ml-auto' : 'bg-gray-100 mr-auto'}`}>
        {text}
    </div>
);
export default ChatMessage;
