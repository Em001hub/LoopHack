import { useState, useEffect } from 'react';
import authService from '../services/auth.service';

export const useAuth = () => {
    const [user, setUser] = useState(null);
    return { user, login: authService.login, logout: authService.logout };
};
