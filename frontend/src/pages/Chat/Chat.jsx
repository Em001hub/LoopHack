import React from 'react';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';
import SuggestedQueries from './SuggestedQueries';

const Chat = () => {
    return (
        <div className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto">
                <ChatMessage text="Hello, how can I help?" isUser={false} />
            </div>
            <SuggestedQueries />
            <ChatInput />
        </div>
    );
};
export default Chat;
