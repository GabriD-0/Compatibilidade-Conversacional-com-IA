import axios, { type AxiosInstance } from 'axios'
import type { DialogoPayload, PostDialogoResponse, ScoreResult } from '../types/api'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

const client: AxiosInstance = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 15000,
})

client.interceptors.response.use(
  (res) => res,
  (err) => {
    const message =
      err.response?.data?.error ||
      err.message ||
      'Erro de conexão com o servidor.'
    return Promise.reject(new Error(message))
  }
)

export const api = {
  async postDialogo(payload: DialogoPayload): Promise<PostDialogoResponse> {
    const { data } = await client.post<PostDialogoResponse>('/api/v1/dialogos', payload)
    return data
  },

  async getDialogos(limit = 50, offset = 0) {
    const { data } = await client.get<{
      dialogos: { id: number; data_criacao: string | null; quantidade_mensagens: number; score: number | null }[]
      limit: number
      offset: number
    }>('/api/v1/dialogos', { params: { limit, offset } })
    return data
  },

  async getDialogo(id: number) {
    const { data } = await client.get(`/api/v1/dialogos/${id}`)
    return data
  },

  async getScore(id: number): Promise<ScoreResult> {
    const { data } = await client.get<ScoreResult>(`/api/v1/dialogos/${id}/score`)
    return data
  },

  async excluirDados(identificador: string) {
    const { data } = await client.delete(`/api/v1/dados/${identificador}`)
    return data
  },
}
