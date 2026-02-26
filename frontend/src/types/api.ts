export interface MensagemPayload {
  autor: string
  texto: string
  timestamp?: string
}

export interface DialogoPayload {
  mensagens: MensagemPayload[]
}

export interface DialogoListItem {
  id: number
  data_criacao: string | null
  quantidade_mensagens: number
  score: number | null
}

export interface DialogoDetail {
  id: number
  data_criacao: string | null
  mensagens: { id: number; autor: string; texto: string; timestamp: string | null }[]
}

export interface ScoreResult {
  score: number
  metricas: {
    lsm?: number
    sentimento?: Record<string, unknown>
    comportamentais?: Record<string, unknown>
  }
  explicabilidade: string[]
  data_calculo?: string | null
}

export interface PostDialogoResponse {
  id: number
  status: string
  score: number
}
