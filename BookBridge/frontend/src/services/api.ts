import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Books API
export const booksAPI = {
  getAll: (skip = 0, limit = 10) => api.get(`/books?skip=${skip}&limit=${limit}`),
  getById: (id: number) => api.get(`/books/${id}`),
  create: (data: any) => api.post('/books', data),
  update: (id: number, data: any) => api.put(`/books/${id}`, data),
  delete: (id: number) => api.delete(`/books/${id}`),
};

// Members API
export const membersAPI = {
  getAll: (skip = 0, limit = 10) => api.get(`/members?skip=${skip}&limit=${limit}`),
  getById: (id: number) => api.get(`/members/${id}`),
  create: (data: any) => api.post('/members', data),
  update: (id: number, data: any) => api.put(`/members/${id}`, data),
  delete: (id: number) => api.delete(`/members/${id}`),
};

// Borrowings API
export const borrowingsAPI = {
  getAll: (skip = 0, limit = 10) => api.get(`/borrowings?skip=${skip}&limit=${limit}`),
  getById: (id: number) => api.get(`/borrowings/${id}`),
  getMemberBorrowings: (memberId: number, isReturned = false) =>
    api.get(`/borrowings/member/${memberId}?is_returned=${isReturned}`),
  borrow: (data: any) => api.post('/borrowings', data),
  returnBook: (id: number) => api.post(`/borrowings/${id}/return`),
  getOverdue: () => api.get('/borrowings/overdue/list'),
};

export default api;
