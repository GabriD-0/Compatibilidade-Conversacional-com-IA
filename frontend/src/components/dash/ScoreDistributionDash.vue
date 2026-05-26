<script setup lang="ts">
import { computed } from 'vue'
import Card from 'primevue/card'
import type { ChartOptions } from 'chart.js'
import { Bar } from 'vue-chartjs'
import type { ScoreDistributionDash } from '../../types/types'
import { dashboardGridColor, dashboardTickColor } from '../../services/chartSetup'

const props = withDefaults(
  defineProps<{
    distribution: ScoreDistributionDash[]
    animationDelay?: string
  }>(),
  {
    animationDelay: '0s',
  },
)

const barData = computed(() => ({
  labels: props.distribution.map((d) => d.range),
  datasets: [
    {
      label: 'Quantidade',
      data: props.distribution.map((d) => d.count),
      backgroundColor: 'hsl(171, 85%, 36%)',
      borderRadius: 4,
      borderSkipped: false,
    },
  ],
}))

const barOptions = computed<ChartOptions<'bar'>>(
  () =>
    ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(36, 36, 36, 0.95)',
          titleColor: '#fff',
          bodyColor: 'rgba(255,255,255,0.85)',
        },
      },
      scales: {
        x: {
          grid: { display: false, drawBorder: false },
          ticks: { color: dashboardTickColor, font: { size: 11 } },
          border: { display: false },
        },
        y: {
          grid: { color: dashboardGridColor, drawBorder: false },
          ticks: { color: dashboardTickColor, font: { size: 11 } },
          border: { display: false },
        },
      },
    }) as ChartOptions<'bar'>,
)
</script>

<template>
  <Card class="dashboard-card dash-animate" :style="{ animationDelay }">
    <template #title>
      <div class="dashboard-card-title">
        <i class="pi pi-chart-bar dashboard-card-title__icon text-secondary" aria-hidden="true"></i>
        <span>Distribuição de Scores</span>
      </div>
    </template>
    <template #content>
      <div class="dashboard-chart-wrap dashboard-chart-wrap--mid">
        <Bar :data="barData" :options="barOptions" />
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

.dashboard-chart-wrap--mid {
  height: 220px;
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
