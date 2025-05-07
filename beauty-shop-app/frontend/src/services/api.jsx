import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000/api', // adjust if using a different port
  withCredentials: true, // if handling auth cookies
});

export default API;
