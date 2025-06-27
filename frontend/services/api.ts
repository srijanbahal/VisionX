import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
// services/api.ts
export const uploadImage = async (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result as string);  // ✅ includes base64
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};


export const processImage = async (algorithm: string, parameters: any, image: string) => {
  const response = await api.post('/process', {
    algorithm,
    parameters,
    image,
  });
  console.log(response.data);
  console.log(image);
  return response.data;
};

export const getProcessingHistory = async () => {
  const response = await api.get('/history');
  return response.data;
};

export default api; 