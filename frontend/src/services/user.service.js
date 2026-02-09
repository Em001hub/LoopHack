import api from './api';

const getProfile = () => api.get('/users/profile');

export default { getProfile };
