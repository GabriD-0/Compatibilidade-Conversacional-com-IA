<script setup lang="ts">
import { computed } from 'vue'
import Card from 'primevue/card'
import type { ChartOptions } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import type { ClassificationDistributionDash } from '../../types/types'
import '../../services/chartSetup'

const props = withDefaults(
  defineProps<{
    distribution: ClassificationDistributionDash[]
    animationDelay?: string
  }>(),
  {
    animationDelay: '0s',
  },
)

function classificationColor(key: string) {
  if (key === 'high') return 'hsl(147, 67%, 60%)'
  if (key === 'mid') return 'hsl(171, 85%, 36%)'
  return 'hsl(330, 96%, 28%)'
}

const pieData = computed(() =>
  props.distribution.map((item) => ({
    name: item.label,
    value: item.value,
    color: classificationColor(item.key),
  })),
)

const doughnutData = computed(() => ({
  labels: pieData.value.map((p) => p.name),
  datasets: [
    {
      data: pieData.value.map((p) => p.value),
      backgroundColor: pieData.value.map((p) => p.color),
      borderWidth: 0,
      hoverOffset: 6,
    },
  ],
}))

const doughnutOptions = computed<ChartOptions<'doughnut'>>(
  () =>
    ({
      responsive: true,
      maintainAspectRatio: false,
      cutout: '55%',
      spacing: 4,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(36, 36, 36, 0.95)',
          titleColor: '#fff',
          bodyColor: 'rgba(255,255,255,0.85)',
        },
      },
    }) as ChartOptions<'doughnut'>,
)
</script>

<template>
  <Card class="dashboard-card dash-animate" :style="{ animationDelay }">
    <template #title>
      <div class="dashboard-card-title">
        <i class="pi pi-bolt dashboard-card-title__icon text-primary" aria-hidden="true"></i>
        <span>Categorias</span>
      </div>
    </template>
    <template #content>
      <div class="dashboard-pie">
        <div class="dashboard-chart-wrap dashboard-chart-wrap--pie">
          <Doughnut :data="doughnutData" :options="doughnutOptions" />
        </div>
        <div class="dashboard-pie__legend">
          <div v-for="d in pieData" :key="d.name" class="dashboard-pie__legend-item">
            <span class="dashboard-pie__dot" :style="{ backgroundColor: d.color }" />
            <span class="dashboard-pie__name">{{ d.name }}</span>
          </div>
        </div>
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

.dashboard-chart-wrap--pie {
  height: 180px;
}

.dashboard-pie {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.dashboard-pie__legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.dashboard-pie__legend-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.75rem;
  color: var(--token-text-muted);
}

.dashboard-pie__dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
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
