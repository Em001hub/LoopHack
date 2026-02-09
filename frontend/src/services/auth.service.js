import api from './api';

const login = (credentials) => api.post('/auth/login', credentials);
const logout = () => api.post('/auth/logout');

export default { login, logout };
