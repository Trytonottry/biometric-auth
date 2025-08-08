import axios from 'axios';

const api = axios.create({
  baseURL: 'http://your-server-ip:5000',
  headers: { 'Content-Type': 'application/json' }
});

export default api;