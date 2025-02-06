import axios, { AxiosError, InternalAxiosRequestConfig, AxiosRequestHeaders } from 'axios';
import { Note } from '@/interface/Note';
import { redirect } from '@tanstack/react-router';

// Interface definitions
interface User {
  userId: number;
  username: string;
  full_name: string;
}

interface AuthResponse {
  user_id: number;
  access_token: string;
  full_name: string;
  refresh_token: string;
}

interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterCredentials extends LoginCredentials {
  full_name: string;
}

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth storage helpers
const getStoredToken = () => localStorage.getItem('token');
const getStoredRefreshToken = () => localStorage.getItem('refresh_token');

const storeAuthData = (authResponse: AuthResponse) => {
  localStorage.setItem('user_id', String(authResponse.user_id));
  localStorage.setItem('token', authResponse.access_token);
  localStorage.setItem('fullname', authResponse.full_name);
  localStorage.setItem('refresh_token', authResponse.refresh_token);
};

const clearAuthData = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user_id');
  localStorage.removeItem('fullname');
};

// Function to refresh token
const refreshToken = async () => {
  const refresh_token = getStoredRefreshToken();
  if (!refresh_token) {
    throw new Error('No refresh token available');
  }

  try {
    const response = await axios.post<AuthResponse>(`${API_BASE_URL}/refresh/`, {
      refresh_token,
    });
    storeAuthData(response.data);
    return response.data.access_token;
  } catch (error) {
    console.error('Failed to refresh token:', error);
    clearAuthData();
    throw redirect({
      to: '/login',
    });
  }
};

// Request interceptor
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = getStoredToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);



api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      const originalRequest = error.config;
      if (!originalRequest) {
        return Promise.reject(error);
      }

      try {
        const newToken = await refreshToken();

        // Create a new headers object
        const headers = {
          ...originalRequest.headers,
          Authorization: `Bearer ${newToken}`,
        };

        // Cast the headers to AxiosRequestHeaders
        originalRequest.headers = headers as AxiosRequestHeaders;

        return api(originalRequest);
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
export const register = async (credentials: RegisterCredentials) => {
  const response = await api.post<AuthResponse>('/register/', credentials);
  storeAuthData(response.data);
  return response.data;
};

export const login = async (credentials: LoginCredentials) => {
  const formData = new FormData();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);

  try {
    const response = await api.post<AuthResponse>('/token/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    // Store authentication data (e.g., tokens)
    storeAuthData(response.data);

    return response.data;
  } catch (err) {
    // Handle API errors
    if (axios.isAxiosError(err)) {
      // If the error is an Axios error, extract the response data
      if (err.response) {
        const errorMessage = err.response.data?.detail || 'Invalid username or password';
        throw new Error(errorMessage); // Throw a meaningful error message
      } else if (err.request) {
        throw new Error('No response received from the server. Please check your connection.');
      }
    } else {
      // Fallback for non-Axios errors
      throw new Error('An unexpected error occurred. Please try again later.');
    }
  }
};

export const logout = () => {
  clearAuthData();
  throw redirect({
    to: '/login',
  });
};

// Protected Note endpoints
export const createNote = async (createdData: Partial<Note>) => {
  const response = await api.post('/note', createdData);
  return response.data;
};

export const getNotes = async () => {
  const response = await api.get('/note/all');
  return response.data;
};

export const updateNote = async (noteId: number, updatedData: Partial<Note>) => {
  const response = await api.put(`/note/${noteId}`, updatedData);
  return response.data;
};

export const deleteNote = async (noteId: number) => {
  await api.delete(`/note/${noteId}`);
};

// Auth helpers
export const isAuthenticated = (): boolean => {
  return !!getStoredToken();
};

export const getCurrentUser = (): User | null => {
  const userStr = localStorage.getItem('user_id');
  return userStr ? JSON.parse(userStr) : null;
};

export default api;
