import axios from 'axios';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'https://textposback.brethren.in/api').replace(/\/$/, '');

export const api = axios.create({ baseURL: API_BASE_URL });
api.interceptors.request.use(c => {
  const t = localStorage.getItem('token');
  if (t) c.headers.Authorization = `Bearer ${t}`;
  return c;
});
export const money = (n:number) => new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR'}).format(n);
