<script setup lang="ts">
import { computed } from 'vue'
import Card from 'primevue/card'
import type { ChartOptions } from 'chart.js'
import { Radar } from 'vue-chartjs'
import type { ProfileMetricDash } from '../../types/types'
import { dashboardGridColor, dashboardTickColor } from '../../services/chartSetup'
import InfoTooltipDash from './InfoTooltipDash.vue'

const props = withDefaults(
  defineProps<{
    profile: ProfileMetricDash[]
    animationDelay?: string
  }>(),
  {
    animationDelay: '0s',
  },
)

const radarChartData = computed(() => ({
  labels: props.profile.map((r) => r.metric),
  datasets: [
    {
      label: 'Valor',
      data: props.profile.map((r) => r.value),
      borderColor: 'hsl(147, 67%, 60%)',
      backgroundColor: 'hsla(147, 67%, 60%, 0.15)',
      borderWidth: 2,
      pointBackgroundColor: 'hsl(147, 67%, 60%)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
    },
  ],
}))

const radarOptions = computed<ChartOptions<'radar'>>(
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
        r: {
          min: 0,
          max: 100,
          angleLines: { color: dashboardGridColor },
          grid: { color: dashboardGridColor },
          pointLabels: {
            color: dashboardTickColor,
            font: { size: 11 },
          },
          ticks: {
            display: false,
            backdropColor: 'transparent',
          },
        },
      },
    }) as ChartOptions<'radar'>,
)
</script>

<template>
  <Card class="dashboard-card dash-animate" :style="{ animationDelay }">
    <template #title>
      <div class="dashboard-card-title">
        <i class="pi pi-bolt dashboard-card-title__icon text-secondary" aria-hidden="true"></i>
        <span>Perfil Médio</span>
        <InfoTooltipDash text="Mostra a média, de 0 a 100, das dimensões avaliadas na analise mais recente de cada par. Valores maiores indicam maior presença da característica medida." />
      </div>
    </template>
    <template #content>
      <div class="dashboard-chart-wrap dashboard-chart-wrap--tall">
        <Radar :data="radarChartData" :options="radarOptions" />
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
