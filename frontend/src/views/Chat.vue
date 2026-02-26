<script setup lang="ts">
import { ref, computed } from 'vue'
import type { MensagemPayload } from '../types/api'
import { api } from '../services/api'
import { useDialogosStore } from '../stores/dialogos'

const store = useDialogosStore()
const mensagens = ref<MensagemPayload[]>([])
const autorAtual = ref('Participante 1')
const textoAtual = ref('')
const enviando = ref(false)
const erro = ref<string | null>(null)

const podeEnviar = computed(() => mensagens.value.length >= 2 && !enviando.value)

function adicionarMensagem() {
  const texto = textoAtual.value.trim()
  if (!texto) return
  const autor = autorAtual.value.trim() || 'Participante 1'
  mensagens.value.push({
    autor,
    texto,
    timestamp: new Date().toISOString(),
  })
  textoAtual.value = ''
}

function removerMensagem(index: number) {
  mensagens.value.splice(index, 1)
}

async function enviarDialogo() {
  if (!podeEnviar.value) return
  enviando.value = true
  erro.value = null
  store.clearError()
  try {
    const res = await api.postDialogo({ mensagens: mensagens.value })
    await store.fetchScore(res.id)
    mensagens.value = []
  } catch (e: unknown) {
    erro.value = e instanceof Error ? e.message : 'Erro ao analisar diálogo.'
  } finally {
    enviando.value = false
  }
}

const scoreResult = computed(() => store.lastScore)
</script>

<template>
  <div class="chat-page">
    <header class="page-header">
      <h1>Chat — Análise de compatibilidade</h1>
      <p class="subtitle">
        Adicione mensagens de dois participantes. O sistema calcula um score de compatibilidade
        conversacional com base em estilo linguístico, sentimentos e dinâmica da conversa.
      </p>
    </header>

    <section class="form-section" aria-label="Adicionar mensagem">
      <div class="form-row">
        <label for="autor">Participante</label>
        <select id="autor" v-model="autorAtual">
          <option value="Participante 1">Participante 1</option>
          <option value="Participante 2">Participante 2</option>
        </select>
      </div>
      <div class="form-row">
        <label for="texto">Mensagem</label>
        <textarea
          id="texto"
          v-model="textoAtual"
          rows="2"
          placeholder="Digite a mensagem..."
          @keydown.enter.prevent="adicionarMensagem"
        />
      </div>
      <button type="button" class="btn btn-secondary" @click="adicionarMensagem">
        Adicionar mensagem
      </button>
    </section>

    <section class="mensagens-section" aria-label="Mensagens do diálogo">
      <h2>Mensagens ({{ mensagens.length }})</h2>
      <p v-if="mensagens.length < 2" class="hint">
        Adicione pelo menos duas mensagens para analisar o diálogo.
      </p>
      <ul v-else class="mensagens-list">
        <li v-for="(m, i) in mensagens" :key="i" class="mensagem-item">
          <span class="autor">{{ m.autor }}:</span>
          <span class="texto">{{ m.texto }}</span>
          <button
            type="button"
            class="btn-remove"
            aria-label="Remover mensagem"
            @click="removerMensagem(i)"
          >
            ×
          </button>
        </li>
      </ul>
      <button
        type="button"
        class="btn btn-primary"
        :disabled="!podeEnviar"
        @click="enviarDialogo"
      >
        {{ enviando ? 'Analisando...' : 'Enviar e analisar diálogo' }}
      </button>
    </section>

    <div v-if="erro || store.error" class="erro" role="alert">
      {{ erro || store.error }}
    </div>

    <section v-if="scoreResult" class="resultado-section" aria-label="Resultado da análise">
      <h2>Resultado da análise</h2>
      <p class="score-desc">
        O score de compatibilidade conversacional varia de 0 a 1: valores mais altos indicam
        maior sintonia entre os participantes (estilo, emoção e equilíbrio de participação).
      </p>
      <div class="score-box">
        <span class="score-value">{{ (scoreResult.score * 100).toFixed(0) }}%</span>
        <span class="score-label">Compatibilidade</span>
      </div>
      <ul v-if="scoreResult.explicabilidade?.length" class="explicabilidade">
        <li v-for="(exp, i) in scoreResult.explicabilidade" :key="i">{{ exp }}</li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.chat-page {
  max-width: 720px;
  margin: 0 auto;
  padding: 1.5rem;
}
.page-header {
  margin-bottom: 1.5rem;
}
.page-header h1 {
  font-size: 1.5rem;
  margin: 0 0 0.5rem 0;
}
.subtitle {
  color: var(--color-text-muted, #666);
  font-size: 0.95rem;
  margin: 0;
}
.form-section,
.mensagens-section,
.resultado-section {
  margin-bottom: 2rem;
}
.form-row {
  margin-bottom: 0.75rem;
}
.form-row label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 500;
}
.form-row select,
.form-row textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font: inherit;
}
.form-row textarea {
  resize: vertical;
  min-height: 60px;
}
.btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font: inherit;
  cursor: pointer;
  border: none;
}
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.btn-secondary {
  background: #e0e0e0;
  color: #333;
}
.btn-primary {
  background: #42b883;
  color: #fff;
  margin-top: 0.75rem;
}
.btn-primary:hover:not(:disabled) {
  background: #359268;
}
.btn-remove {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0 0.25rem;
  margin-left: auto;
}
.btn-remove:hover {
  color: #c00;
}
.mensagens-list {
  list-style: none;
  padding: 0;
  margin: 0 0 1rem 0;
}
.mensagem-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #eee;
  border-radius: 6px;
  margin-bottom: 0.5rem;
}
.autor {
  font-weight: 600;
  flex-shrink: 0;
}
.texto {
  flex: 1;
  word-break: break-word;
}
.hint {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 1rem 0;
}
.erro {
  color: #c00;
  padding: 0.75rem;
  background: #fee;
  border-radius: 6px;
  margin-bottom: 1rem;
}
.resultado-section h2 {
  font-size: 1.2rem;
  margin: 0 0 0.5rem 0;
}
.score-desc {
  font-size: 0.9rem;
  color: #555;
  margin: 0 0 1rem 0;
}
.score-box {
  display: inline-flex;
  flex-direction: column;
  padding: 1rem 1.5rem;
  background: #e8f5e9;
  border-radius: 8px;
  margin-bottom: 1rem;
}
.score-value {
  font-size: 2rem;
  font-weight: 700;
  color: #2e7d32;
}
.score-label {
  font-size: 0.85rem;
  color: #555;
}
.explicabilidade {
  list-style: disc;
  padding-left: 1.5rem;
  margin: 0;
  color: #333;
}
.explicabilidade li {
  margin-bottom: 0.25rem;
}
</style>
