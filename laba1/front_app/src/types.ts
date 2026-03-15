export type Role = 'admin' | 'moderator' | 'viewer'

export interface User {
  id: number
  username: string
  email: string
  role: Role
  is_active: boolean
}

export interface Token {
  access_token: string
  token_type: string
  exp: string | null
}

export interface Item {
  id: number
  title: string
  description: string | null
}

export interface ItemCreate {
  title: string
  description?: string | null
}

export interface ItemUpdate {
  title?: string
  description?: string | null
}
