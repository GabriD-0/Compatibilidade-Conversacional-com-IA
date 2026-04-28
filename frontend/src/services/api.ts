import axios from 'axios'
import type { RefreshResponse, ConversationsPage, Conversation, MessagesPage } from '../types/api'

const ACCESS_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'

let isRefreshing = false
let refreshQueue: Array<(token: string) => void> = []

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_KEY)
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    const code = error.response?.data?.error?.code

    if (error.response?.status === 401 && !original._retry && code === 'token_expired') {
      original._retry = true

      if (isRefreshing) {
        return new Promise((resolve) => {
          refreshQueue.push((newToken) => {
            original.headers.Authorization = `Bearer ${newToken}`
            resolve(api(original))
          })
        })
      }

      isRefreshing = true
      try {
        const refreshToken = localStorage.getItem(REFRESH_KEY)
        const { data } = await axios.post<RefreshResponse>(
          `${import.meta.env.VITE_API_BASE_URL}/api/auth/refresh`,
          { refresh_token: refreshToken },
          { headers: { Authorization: `Bearer ${refreshToken}` } },
        )

        localStorage.setItem(ACCESS_KEY, data.access_token)
        refreshQueue.forEach((cb) => cb(data.access_token))
        refreshQueue = []
        original.headers.Authorization = `Bearer ${data.access_token}`

        return api(original)

      } catch {
        refreshQueue = []
        localStorage.removeItem(ACCESS_KEY)
        localStorage.removeItem(REFRESH_KEY)
        localStorage.removeItem('user')
        window.location.href = '/login'
        return Promise.reject(error)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  },
)

// ---- Conversation endpoints ----

export const conversationsApi = {
  list(page = 1, perPage = 20): Promise<ConversationsPage> {
    return api.get('/api/conversations', { params: { page, per_page: perPage } }).then((r) => r.data)
  },

  create(): Promise<Conversation> {
    return api.post('/api/conversations').then((r) => r.data)
  },

  get(id: number): Promise<Conversation> {
    return api.get(`/api/conversations/${id}`).then((r) => r.data)
  },

  messages(conversationId: number, afterPosition = 0, limit = 50): Promise<MessagesPage> {
    return api
      .get(`/api/conversations/${conversationId}/messages`, {
        params: { after_position: afterPosition, limit },
      })
      .then((r) => r.data)
  },

  delete(id: number): Promise<void> {
    return api.delete(`/api/conversations/${id}`).then(() => undefined)
  },
}

export function extractApiError(err: unknown): string {
  if (axios.isAxiosError(err)) {
    const msg = err.response?.data?.error?.message
    if (msg) return msg as string
  }
  return 'Ocorreu um erro inesperado. Tente novamente.'
}