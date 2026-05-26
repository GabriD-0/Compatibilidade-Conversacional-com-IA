<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import Card from 'primevue/card'
import type { ChartOptions } from 'chart.js'
import { Line } from 'vue-chartjs'
import type { EmotionalConversationDash } from '../../types/types'
import { dashboardGridColor, dashboardTickColor } from '../../services/chartSetup'

const props = withDefaults(
  defineProps<{
    conversations: EmotionalConversationDash[]
    animationDelay?: string
  }>(),
  {
    animationDelay: '0s',
  },
)

const selectedConversationId = ref<number | null>(null)

const selectedConversation = computed(() => {
  if (!props.conversations.length) return null
  return (
    props.conversations.find((conversation) => conversation.conversation_id === selectedConversationId.value) ??
    props.conversations[0]
  )
})

watch(
  () => props.conversations,
  (conversations) => {
    if (!conversations.length) {
      selectedConversationId.value = null
      return
    }

    const currentStillExists = conversations.some(
      (conversation) => conversation.conversation_id === selectedConversationId.value,
    )
    const firstConversation = conversations[0]
    if (!currentStillExists && firstConversation) {
      selectedConversationId.value = firstConversation.conversation_id
    }
  },
  { immediate: true },
)

const emotionalLineData = computed(() => ({
  labels: selectedConversation.value?.points.map((d) => `M${d.msg}`) ?? [],
  datasets: [
    {
      label: selectedConversation.value?.person_a ?? 'Pessoa A',
      data: selectedConversation.value?.points.map((d) => d.person_a) ?? [],
      borderColor: 'hsl(147, 67%, 60%)',
      backgroundColor: 'transparent',
      tension: 0.35,
      borderWidth: 2,
      pointRadius: 3,
      pointBackgroundColor: 'hsl(147, 67%, 60%)',
      spanGaps: true,
    },
    {
      label: selectedConversation.value?.person_b ?? 'Pessoa B',
      data: selectedConversation.value?.points.map((d) => d.person_b) ?? [],
      borderColor: 'hsl(330, 96%, 28%)',
      backgroundColor: 'transparent',
      borderDash: [5, 5],
      tension: 0.35,
      borderWidth: 2,
      pointRadius: 3,
      pointBackgroundColor: 'hsl(330, 96%, 28%)',
      spanGaps: true,
    },
  ],
}))

const emotionalLineOptions = computed<ChartOptions<'line'>>(
  () =>
    ({
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: {
            color: 'rgba(255, 255, 255, 0.6)',
            boxWidth: 10,
            boxHeight: 10,
            padding: 12,
            font: { size: 11 },
          },
        },
        tooltip: {
          backgroundColor: 'rgba(36, 36, 36, 0.95)',
          titleColor: '#fff',
          bodyColor: 'rgba(255,255,255,0.85)',
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Mensagem',
            color: 'rgba(255, 255, 255, 0.4)',
            font: { size: 10 },
            padding: { top: 8 },
          },
          grid: { color: dashboardGridColor, drawBorder: false },
          ticks: { color: dashboardTickColor, font: { size: 11 }, maxRotation: 0 },
          border: { display: false },
        },
        y: {
          min: -1,
          max: 1,
          grid: { color: dashboardGridColor, drawBorder: false },
          ticks: { color: dashboardTickColor, font: { size: 11 } },
          border: { display: false },
        },
      },
    }) as ChartOptions<'line'>,
)
</script>

<template>
  <Card class="dashboard-card dash-animate" :style="{ animationDelay }">
    <template #title>
      <div class="dashboard-card-head">
        <div class="dashboard-card-title">
          <i class="pi pi-heart dashboard-card-title__icon text-accent" aria-hidden="true"></i>
          <span>Convergencia Emocional</span>
        </div>
        <select
          v-if="conversations.length > 1"
          v-model.number="selectedConversationId"
          class="dashboard-card-select"
          aria-label="Selecionar match"
        >
          <option
            v-for="conversation in conversations"
            :key="conversation.conversation_id"
            :value="conversation.conversation_id"
          >
            {{ conversation.label }}
          </option>
        </select>
      </div>
    </template>
    <template #content>
      <div v-if="selectedConversation" class="dashboard-chart-wrap dashboard-chart-wrap--tall">
        <Line :data="emotionalLineData" :options="emotionalLineOptions" />
      </div>
      <p v-else class="dashboard-empty">Nenhum dado emocional disponivel.</p>
    </template>
  </Card>
</template>

<style scoped>
.dashboard-card {
  background: color-mix(in srgb, var(--token-bg-surface) 50%, transparent) !important;
  backdrop-filter: blur(12px);
  border: 1px solid color-mix(in srgb, var(--token-border) 50%, transparent) !important;
  transition: border-color 0.2s;
}

.dashboard-card:hover {
  border-color: color-mix(in srgb, var(--color-primary) 30%, transparent) !important;
}

.dashboard-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.dashboard-card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
}

.dashboard-card-title__icon {
  font-size: 1rem;
}

.dashboard-card-select {
  min-width: 11rem;
  max-width: 16rem;
  min-height: 2rem;
  padding: 0.35rem 0.55rem;
  border-radius: 0.45rem;
  border: 1px solid color-mix(in srgb, var(--token-border) 42%, transparent);
  color: var(--token-text);
  background: color-mix(in srgb, var(--token-bg-page) 45%, transparent);
  font: inherit;
  font-size: 0.78rem;
  outline: none;
}

.dashboard-card-select:focus {
  border-color: var(--color-primary);
}

.dashboard-chart-wrap {
  position: relative;
  width: 100%;
}

.dashboard-chart-wrap--tall {
  height: 280px;
}

.dashboard-empty {
  margin: 0;
  padding: 1rem;
  border-radius: 0.5rem;
  color: var(--token-text-muted);
  background: color-mix(in srgb, var(--token-bg-page) 30%, transparent);
  border: 1px solid color-mix(in srgb, var(--token-border) 20%, transparent);
  font-size: 0.82rem;
}

.dash-animate {
  opacity: 0;
  animation: dashFadeUp 0.55s ease forwards;
}

@keyframes dashFadeUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 640px) {
  .dashboard-card-head {
    align-items: stretch;
    flex-direction: column;
  }

  .dashboard-card-select {
    max-width: none;
    width: 100%;
  }
}
</style>
