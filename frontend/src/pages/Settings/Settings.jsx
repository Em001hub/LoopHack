import React from 'react';
import Integrations from './Integrations';
import Notifications from './Notifications';
import Team from './Team';

const Settings = () => {
    return (
        <div>
            <h2>Settings</h2>
            <Integrations />
            <Notifications />
            <Team />
        </div>
    );
};
export default Settings;
