<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { useDialogosStore } from '../stores/dialogos'
import { api } from '../services/api'
import type { ScoreResult } from '../types/api'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const store = useDialogosStore()
const detalheId = ref<number | null>(null)
const detalheScore = ref<ScoreResult | null>(null)
const carregandoDetalhe = ref(false)

onMounted(() => {
  store.fetchDialogos().catch(() => {})
})

const dialogos = computed(() => store.dialogos)
const loading = computed(() => store.loading)
const error = computed(() => store.error)

const topN = computed(() => {
  return [...dialogos.value]
    .filter((d) => d.score != null)
    .sort((a, b) => (b.score ?? 0) - (a.score ?? 0))
    .slice(0, 10)
})

const faixas = computed(() => {
  const bins: number[] = [0, 0.2, 0.4, 0.6, 0.8, 1.01]
  const labels = ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%']
  const counts: number[] = [0, 0, 0, 0, 0]
  for (const d of dialogos.value) {
    const s = d.score ?? 0
    for (let i = 0; i < bins.length - 1; i++) {
      const lo = bins[i]!
      const hi = bins[i + 1]!
      if (s >= lo && s < hi) {
        counts[i] = (counts[i] ?? 0) + 1
        break
      }
    }
  }
  return { labels, counts }
})

const chartData = computed(() => ({
  labels: faixas.value.labels,
  datasets: [
    {
      label: 'Quantidade de diálogos',
      data: faixas.value.counts,
      backgroundColor: 'rgba(66, 184, 131, 0.7)',
      borderColor: 'rgb(66, 184, 131)',
      borderWidth: 1,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: { beginAtZero: true, ticks: { stepSize: 1 } },
  },
  plugins: {
    legend: { display: false },
    title: { display: true, text: 'Distribuição dos scores de compatibilidade' },
  },
}

async function abrirDetalhe(id: number) {
  detalheId.value = id
  detalheScore.value = null
  carregandoDetalhe.value = true
  try {
    detalheScore.value = await api.getScore(id)
  } catch {
    detalheScore.value = null
  } finally {
    carregandoDetalhe.value = false
  }
}

function fecharDetalhe() {
  detalheId.value = null
  detalheScore.value = null
}
</script>

<template>
  <div class="dashboard-page">
    <header class="page-header">
      <h1>Dashboard — Métricas e compatibilidade</h1>
      <p class="subtitle">
        Visualize a distribuição dos scores e os detalhes de cada análise. O score reflete
        a sintonia conversacional (estilo linguístico, sentimentos e equilíbrio de participação).
      </p>
    </header>

    <div v-if="error" class="erro" role="alert">{{ error }}</div>

    <section class="chart-section" aria-label="Distribuição de scores">
      <h2>Distribuição de scores</h2>
      <div class="chart-container">
        <Bar v-if="chartData.datasets[0]?.data?.some((v) => v > 0)" :data="chartData" :options="chartOptions" />
        <p v-else class="empty-hint">Nenhum diálogo analisado ainda. Use a tela Chat para enviar um diálogo.</p>
      </div>
    </section>

    <section class="list-section" aria-label="Top análises">
      <h2>Top análises (maior compatibilidade)</h2>
      <p v-if="loading && dialogos.length === 0">Carregando...</p>
      <ul v-else-if="topN.length === 0" class="empty-list">
        Nenhum resultado disponível.
      </ul>
      <ul v-else class="dialogos-list">
        <li
          v-for="d in topN"
          :key="d.id"
          class="dialogo-card"
          :class="{ selected: detalheId === d.id }"
          @click="abrirDetalhe(d.id)"
        >
          <span class="id">#{{ d.id }}</span>
          <span class="score">{{ d.score != null ? (d.score * 100).toFixed(0) + '%' : '—' }}</span>
          <span class="meta">{{ d.quantidade_mensagens }} msgs</span>
        </li>
      </ul>
    </section>

    <div v-if="detalheId !== null" class="modal-overlay" role="dialog" aria-modal="true" aria-label="Detalhe da análise" @click.self="fecharDetalhe">
      <div class="modal">
        <button type="button" class="btn-close" aria-label="Fechar" @click="fecharDetalhe">×</button>
        <h3>Detalhe do diálogo #{{ detalheId }}</h3>
        <p v-if="carregandoDetalhe">Carregando...</p>
        <template v-else-if="detalheScore">
          <div class="score-box">
            <span class="score-value">{{ (detalheScore.score * 100).toFixed(0) }}%</span>
            <span class="score-label">Compatibilidade</span>
          </div>
          <div v-if="detalheScore.metricas" class="metricas">
            <p v-if="detalheScore.metricas.lsm != null">
              <strong>LSM (estilo):</strong> {{ (detalheScore.metricas.lsm * 100).toFixed(0) }}%
            </p>
            <p v-if="detalheScore.metricas.comportamentais">
              <strong>Comportamentais:</strong> equilíbrio de turnos, latência, comprimento médio.
            </p>
          </div>
          <ul v-if="detalheScore.explicabilidade?.length" class="explicabilidade">
            <li v-for="(exp, i) in detalheScore.explicabilidade" :key="i">{{ exp }}</li>
          </ul>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-page {
  max-width: 960px;
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
.erro {
  color: #c00;
  padding: 0.75rem;
  background: #fee;
  border-radius: 6px;
  margin-bottom: 1rem;
}
.chart-section,
.list-section {
  margin-bottom: 2rem;
}
.chart-section h2,
.list-section h2 {
  font-size: 1.2rem;
  margin: 0 0 0.75rem 0;
}
.chart-container {
  height: 280px;
  background: #fafafa;
  border-radius: 8px;
  padding: 1rem;
}
.empty-hint {
  color: #666;
  padding: 2rem;
  margin: 0;
  text-align: center;
}
.empty-list {
  list-style: none;
  padding: 0;
  margin: 0;
  color: #666;
}
.dialogos-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 0.75rem;
}
.dialogo-card {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  border: 2px solid #eee;
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.dialogo-card:hover,
.dialogo-card.selected {
  border-color: #42b883;
  background: #f0faf5;
}
.id {
  font-weight: 600;
  color: #555;
}
.score {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2e7d32;
  margin: 0.25rem 0;
}
.meta {
  font-size: 0.85rem;
  color: #888;
}
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}
.modal {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 480px;
  width: 100%;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}
.btn-close {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}
.btn-close:hover {
  color: #000;
}
.modal h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
}
.score-box {
  display: inline-flex;
  flex-direction: column;
  padding: 0.75rem 1.25rem;
  background: #e8f5e9;
  border-radius: 8px;
  margin-bottom: 1rem;
}
.score-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2e7d32;
}
.score-label {
  font-size: 0.85rem;
  color: #555;
}
.metricas {
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #444;
}
.metricas p {
  margin: 0.25rem 0;
}
.explicabilidade {
  list-style: disc;
  padding-left: 1.5rem;
  margin: 0;
}
.explicabilidade li {
  margin-bottom: 0.25rem;
}
</style>
