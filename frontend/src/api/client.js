import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Upload APIs
export const uploadCircular = (file, source = 'RBI') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('source', source);
  return client.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getCirculars = () => client.get('/upload/circulars');
export const getCircular = (id) => client.get(`/upload/circulars/${id}`);

// Extraction APIs
export const triggerExtraction = (circularId) => client.post(`/extract/${circularId}`);
export const getRules = (circularId) => client.get(`/extract/${circularId}/rules`);
export const getConflicts = (circularId) => client.get(`/extract/${circularId}/conflicts`);

// Task APIs
export const getTasks = (filters = {}) => {
  const params = new URLSearchParams();
  if (filters.department) params.append('department', filters.department);
  if (filters.status) params.append('status', filters.status);
  if (filters.priority) params.append('priority', filters.priority);
  if (filters.circular_id) params.append('circular_id', filters.circular_id);
  return client.get(`/tasks?${params.toString()}`);
};

export const getTaskStats = () => client.get('/tasks/stats');
export const getTask = (id) => client.get(`/tasks/${id}`);
export const updateTask = (id, updates) => client.patch(`/tasks/${id}`, updates);

// Verification APIs
export const runVerification = () => client.post('/verify/run');
export const getVerificationSummary = () => client.get('/verify/summary');
export const getTaskVerification = (taskId) => client.get(`/verify/task/${taskId}`);

// Health check
export const healthCheck = () => client.get('/health');

export default client;
