import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { api } from '../services/api'
import type { AuthUser, AuthResponse } from '../types/api'

const ACCESS_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'
const USER_KEY = 'user'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<AuthUser | null>(JSON.parse(localStorage.getItem(USER_KEY) ?? 'null'),)
  const accessToken = ref<string | null>(localStorage.getItem(ACCESS_KEY))
  const refreshToken = ref<string | null>(localStorage.getItem(REFRESH_KEY))

  const isAuthenticated = computed(() => user.value !== null && accessToken.value !== null)

  async function login(email: string, password: string): Promise<void> {
    const { data } = await api.post<AuthResponse>('/api/auth/login', { email, password })
    persist(data)
  }

  async function register(name: string, email: string, password: string): Promise<void> {
    const { data } = await api.post<AuthResponse>('/api/auth/register', { name, email, password })
    persist(data)
  }

  function logout(): void {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem(ACCESS_KEY)
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(USER_KEY)
  }

  function persist(data: AuthResponse): void {
    user.value = data.user
    accessToken.value = data.access_token
    refreshToken.value = data.refresh_token
    localStorage.setItem(ACCESS_KEY, data.access_token)
    localStorage.setItem(REFRESH_KEY, data.refresh_token)
    localStorage.setItem(USER_KEY, JSON.stringify(data.user))
  }

  return { user, accessToken, refreshToken, isAuthenticated, login, register, logout }
})