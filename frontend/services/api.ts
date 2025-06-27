import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadImage = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const processImage = async (algorithm: string, parameters: any, image: string) => {
  const response = await api.post('/process', {
    algorithm,
    parameters,
    image,
  });
  return response.data;
};

export const getProcessingHistory = async () => {
  const response = await api.get('/history');
  return response.data;
};

export default api; 