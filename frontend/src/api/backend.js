import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000'; // Update if backend is on a different port/host

export const uploadFiles = async (files) => {
  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append('files', files[i]);
  }
  return axios.post(`${API_BASE}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const trainModel = async () => axios.post(`${API_BASE}/train`);
export const generateXAI = async () => axios.post(`${API_BASE}/xai`);
export const getResults = async () => axios.get(`${API_BASE}/results`);
