import { api } from './client'
import type { User } from '../types'

export function login(username: string, password: string) {
  const form = new FormData()
  form.append('username', username)
  form.append('password', password)
  return api<{ access_token: string; token_type: string }>('/api/auth/login', {
    method: 'POST',
    formData: form,
  })
}

export function register(data: {
  username: string
  email: string
  password: string
  role?: string
}) {
  return api<User>('/api/auth/register', {
    method: 'POST',
    body: { ...data, role: data.role || 'viewer' },
  })
}

export function getMe() {
  return api<User>('/api/auth/me')
}
