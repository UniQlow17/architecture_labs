const API_BASE = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')

export function getToken(): string | null {
  return localStorage.getItem('token')
}

export type ApiOptions = Omit<RequestInit, 'body'> & {
  body?: object
  formData?: FormData
}

export async function api<T>(
  path: string,
  options: ApiOptions = {}
): Promise<T> {
  const { body, formData, ...rest } = options
  const headers: HeadersInit = {}
  const token = getToken()
  if (token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`
  }
  if (formData) {
    const res = await fetch(`${API_BASE}${path}`, {
      ...rest,
      body: formData,
      headers: rest.headers ? { ...headers, ...rest.headers } : headers,
    })
    await handleStatus(res)
    return res.json() as Promise<T>
  }
  if (body != null) {
    (headers as Record<string, string>)['Content-Type'] = 'application/json'
  }
  const res = await fetch(`${API_BASE}${path}`, {
    ...rest,
    body: body != null ? JSON.stringify(body) : undefined,
    headers: rest.headers ? { ...headers, ...rest.headers } : headers,
  })
  if (res.status === 204) return undefined as T
  await handleStatus(res)
  return res.json() as Promise<T>
}

function formatDetail(detail: unknown): string {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail
      .map((e: { msg?: string; loc?: unknown }) => e?.msg ?? JSON.stringify(e))
      .filter(Boolean)
      .join('. ')
  }
  if (detail && typeof detail === 'object' && 'message' in detail) {
    return String((detail as { message: unknown }).message)
  }
  return String(detail ?? '')
}

async function handleStatus(res: Response): Promise<void> {
  if (res.ok) return
  const text = await res.text()
  let message: string
  try {
    const j = JSON.parse(text)
    const detail = j.detail ?? text
    message = formatDetail(detail) || res.statusText
  } catch {
    message = text || res.statusText
  }
  throw new ApiError(res.status, message)
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export function getErrorMessage(err: unknown, fallback: string): string {
  if (err instanceof ApiError) return err.message
  if (err instanceof Error) return err.message
  if (typeof err === 'string') return err
  return fallback
}
