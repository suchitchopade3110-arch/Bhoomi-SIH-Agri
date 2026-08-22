export const env = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  kvkCenter: import.meta.env.VITE_KVK_CENTER || 'ICAR-KVK Erode / MYRADA Center',
  environment: import.meta.env.MODE || 'development',
};
