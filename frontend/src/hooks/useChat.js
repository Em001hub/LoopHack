import { useState } from 'react';
export const useChat = () => {
    const [messages, setMessages] = useState([]);
    return { messages, sendMessage: (msg) => { } };
};
