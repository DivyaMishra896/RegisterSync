import axios from 'axios';

export const API_BASE = 'http://localhost:8000/api';

// Heavy client — for upload/extraction which can take minutes with Ollama
const client = axios.create({
  baseURL: API_BASE,
  timeout: 300000, // 5 minutes for Ollama inference
  headers: {
    'Content-Type': 'application/json',
  },
});

// Fast client — for quick DB reads (tasks, stats, circulars, health)
const fastClient = axios.create({
  baseURL: API_BASE,
  timeout: 15000, // 15 seconds max for simple queries
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadCircular = (file, source = 'RBI') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('source', source);
  return client.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getCirculars = () => fastClient.get('/upload/circulars');
export const getCircular = (id) => fastClient.get(`/upload/circulars/${id}`);

export const triggerExtraction = (circularId) => client.post(`/extract/${circularId}`);
export const getRules = (circularId) => fastClient.get(`/extract/${circularId}/rules`);
export const getConflicts = (circularId) => fastClient.get(`/extract/${circularId}/conflicts`);

export const getTasks = (filters = {}) => {
  const params = new URLSearchParams();
  if (filters.department) params.append('department', filters.department);
  if (filters.status) params.append('status', filters.status);
  if (filters.priority) params.append('priority', filters.priority);
  if (filters.circular_id) params.append('circular_id', filters.circular_id);
  return fastClient.get(`/tasks?${params.toString()}`);
};

export const getTaskStats = () => fastClient.get('/tasks/stats');
export const getTask = (id) => fastClient.get(`/tasks/${id}`);
export const updateTask = (id, updates) => fastClient.patch(`/tasks/${id}`, updates);

export const runVerification = () => client.post('/verify/run');
export const getVerificationSummary = () => fastClient.get('/verify/summary');
export const getTaskVerification = (taskId) => fastClient.get(`/verify/task/${taskId}`);

export const healthCheck = () => fastClient.get('/health');

export default client;

