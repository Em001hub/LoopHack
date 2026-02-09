import api from './api';

const getAll = () => api.get('/projects').then(res => res.data);

export default { getAll };
