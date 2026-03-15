import { api } from './client'
import type { Item, ItemCreate, ItemUpdate } from '../types'

export function getItems(offset = 0, limit = 20) {
  return api<Item[]>(`/api/items?offset=${offset}&limit=${limit}`)
}

export function getItem(id: number) {
  return api<Item>(`/api/items/${id}`)
}

export function createItem(data: ItemCreate) {
  return api<Item>('/api/items', { method: 'POST', body: data })
}

export function updateItem(id: number, data: ItemUpdate) {
  return api<Item>(`/api/items/${id}`, { method: 'PATCH', body: data })
}

export function deleteItem(id: number) {
  return api<void>(`/api/items/${id}`, { method: 'DELETE' })
}
