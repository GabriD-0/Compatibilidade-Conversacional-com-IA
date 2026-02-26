import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { DialogoListItem, ScoreResult } from '../types/api'
import { api } from '../services/api'

export const useDialogosStore = defineStore('dialogos', () => {
  const dialogos = ref<DialogoListItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const lastScore = ref<ScoreResult | null>(null)

  async function fetchDialogos(limit = 50, offset = 0) {
    loading.value = true
    error.value = null
    try {
      const res = await api.getDialogos(limit, offset)
      dialogos.value = res.dialogos
      return res
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Erro ao carregar diálogos'
      error.value = msg
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchScore(dialogoId: number) {
    loading.value = true
    error.value = null
    try {
      const res = await api.getScore(dialogoId)
      lastScore.value = res
      return res
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Erro ao carregar score'
      error.value = msg
      throw e
    } finally {
      loading.value = false
    }
  }

  function setLastScore(result: ScoreResult | null) {
    lastScore.value = result
  }

  function clearError() {
    error.value = null
  }

  return {
    dialogos,
    loading,
    error,
    lastScore,
    fetchDialogos,
    fetchScore,
    setLastScore,
    clearError,
  }
})
