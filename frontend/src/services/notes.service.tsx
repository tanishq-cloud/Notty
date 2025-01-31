import axios from 'axios';
import { Note } from '@/interface/Note'
const API_BASE_URL = 'http://localhost:4500/notes';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getNotes = async () => {
  const response = await api.get('/notes');
  return response.data;
};

export const updateNote = async (noteId: number, updatedData: Partial<Note>) => {
  const response = await api.put(`/notes/${noteId}`, updatedData);
  return response.data;
};

export const deleteNote = async (noteId: number) => {
  await api.delete(`/notes/${noteId}`);
};

export default api;
