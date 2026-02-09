import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard/Dashboard';
import IntelligenceDashboard from './pages/IntelligenceDashboard';
import ConversationIntelligence from './pages/ConversationIntelligence';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<MainLayout><Dashboard /></MainLayout>} />
                <Route path="/intelligence" element={<IntelligenceDashboard />} />
                <Route path="/conversation" element={<ConversationIntelligence />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;


