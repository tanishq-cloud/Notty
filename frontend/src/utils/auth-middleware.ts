// src/utils/authMiddleware.ts
import { redirect } from '@tanstack/react-router';

export function authMiddleware() {
  const token = localStorage.getItem('token');
  if (!token) {
    throw redirect({
      to: '/login',
      search: {
        redirect: window.location.pathname,
      },
    });
  }
}