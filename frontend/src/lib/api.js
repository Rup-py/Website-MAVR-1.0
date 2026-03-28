import axios from 'axios';

const API = process.env.REACT_APP_BACKEND_URL;

// Configure axios defaults
axios.defaults.withCredentials = true;

export const api = {
  // Dashboard
  getDashboard: () => axios.get(`${API}/api/dashboard`),
  
  // Diet
  getTodayDiet: () => axios.get(`${API}/api/diet/today`),
  getDietHistory: (days = 7) => axios.get(`${API}/api/diet/history?days=${days}`),
  
  // Workout
  getTodayWorkout: () => axios.get(`${API}/api/workout/today`),
  logWorkout: (data) => axios.post(`${API}/api/workout/log`, data),
  
  // Check-ins
  morningCheckin: (data) => axios.post(`${API}/api/checkin/morning`, data),
  workoutCheckin: (data) => axios.post(`${API}/api/checkin/workout`, data),
  nightCheckin: (data) => axios.post(`${API}/api/checkin/night`, data),
  
  // Onboarding
  saveOnboarding: (profileData) => axios.post(`${API}/api/onboarding/save`, { profile_data: profileData }),
  getProfile: () => axios.get(`${API}/api/onboarding/profile`),
  
  // Progression
  getProgressionSummary: (days = 30) => axios.get(`${API}/api/progression/summary?days=${days}`),
  
  // Events
  createEvent: (data) => axios.post(`${API}/api/event/create`, data),
  getActiveEvent: () => axios.get(`${API}/api/event/active`),
  deactivateEvent: (eventId) => axios.post(`${API}/api/event/${eventId}/deactivate`),
  
  // Reports
  getWeeklyReport: () => axios.get(`${API}/api/reports/weekly`),
  
  // Admin
  adminGetUsers: (skip = 0, limit = 50) => axios.get(`${API}/api/admin/users?skip=${skip}&limit=${limit}`),
  adminGetAnalytics: () => axios.get(`${API}/api/admin/analytics`),
  adminGetUserDetail: (userId) => axios.get(`${API}/api/admin/user/${userId}`),
  
  // Products
  getProducts: (category, bodyStage) => {
    let url = `${API}/api/products`;
    const params = [];
    if (category) params.push(`category=${category}`);
    if (bodyStage) params.push(`body_stage=${bodyStage}`);
    if (params.length) url += `?${params.join('&')}`;
    return axios.get(url);
  },
};

export default api;
