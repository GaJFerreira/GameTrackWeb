import axios from 'axios';

const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: baseURL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {

    if (error.response && error.response.status === 401) {
      console.warn("Sessão expirada. Realizando logout automático.");
      
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;