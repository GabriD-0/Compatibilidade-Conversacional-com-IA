<script setup lang="ts">
import { computed } from 'vue'
import Card from 'primevue/card'
import type { ChartOptions } from 'chart.js'
import { Line } from 'vue-chartjs'
import type { WeeklyScoreDash } from '../../types/types'
import { dashboardGridColor, dashboardTickColor } from '../../services/chartSetup'

const props = withDefaults(
  defineProps<{
    weeklyScores: WeeklyScoreDash[]
    animationDelay?: string
  }>(),
  {
    animationDelay: '0s',
  },
)

const convColor = 'hsl(171, 85%, 42%)'

const lineData = computed(() => ({
  labels: props.weeklyScores.map((d) => d.day),
  datasets: [
    {
      label: 'Score',
      data: props.weeklyScores.map((d) => d.score),
      yAxisID: 'y',
      borderColor: 'hsl(147, 67%, 60%)',
      backgroundColor: 'rgba(90, 219, 148, 0.2)',
      fill: true,
      tension: 0.35,
      borderWidth: 2,
      pointRadius: 3,
      pointBackgroundColor: 'hsl(147, 67%, 60%)',
      spanGaps: true,
      order: 2,
    },
    {
      label: 'Conversas',
      data: props.weeklyScores.map((d) => d.conversations),
      yAxisID: 'y1',
      borderColor: convColor,
      backgroundColor: 'transparent',
      fill: false,
      tension: 0.35,
      borderWidth: 2,
      pointRadius: 3,
      pointBackgroundColor: convColor,
      order: 1,
    },
  ],
}))

const lineOptions = computed<ChartOptions<'line'>>(
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
            color: dashboardTickColor,
            boxWidth: 10,
            boxHeight: 10,
            padding: 16,
            font: { size: 11 },
          },
        },
        tooltip: {
          backgroundColor: 'rgba(36, 36, 36, 0.95)',
          titleColor: '#fff',
          bodyColor: 'rgba(255,255,255,0.85)',
          borderColor: 'rgba(90, 219, 148, 0.35)',
          borderWidth: 1,
        },
      },
      scales: {
        x: {
          grid: { color: dashboardGridColor, drawBorder: false },
          ticks: { color: dashboardTickColor, font: { size: 12 } },
          border: { display: false },
        },
        y: {
          id: 'y',
          type: 'linear',
          position: 'left',
          min: 0,
          max: 100,
          grid: { color: dashboardGridColor, drawBorder: false },
          ticks: { color: dashboardTickColor, font: { size: 12 } },
          border: { display: false },
        },
        y1: {
          id: 'y1',
          type: 'linear',
          position: 'right',
          min: 0,
          suggestedMax: Math.max(5, ...props.weeklyScores.map((d) => d.conversations + 2)),
          grid: { drawOnChartArea: false },
          ticks: {
            color: convColor,
            font: { size: 11 },
          },
          border: { display: false },
        },
      },
    }) as ChartOptions<'line'>,
)
</script>

<template>
  <Card class="dashboard-card dashboard-card--wide dash-animate" :style="{ animationDelay }">
    <template #title>
      <div class="dashboard-card-title">
        <i class="pi pi-chart-line dashboard-card-title__icon text-primary" aria-hidden="true"></i>
        <span>Evolução do Score Semanal</span>
      </div>
    </template>
    <template #content>
      <div class="dashboard-chart-wrap dashboard-chart-wrap--tall">
        <Line :data="lineData" :options="lineOptions" />
      </div>
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

.dashboard-card--wide {
  grid-column: span 1;
}

@media (min-width: 1024px) {
  .dashboard-card--wide {
    grid-column: span 2;
  }
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

.dashboard-chart-wrap {
  position: relative;
  width: 100%;
}

.dashboard-chart-wrap--tall {
  height: 280px;
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
</style>
