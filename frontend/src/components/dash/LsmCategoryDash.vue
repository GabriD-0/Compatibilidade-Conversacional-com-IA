<script setup lang="ts">
import { computed } from 'vue'
import Card from 'primevue/card'
import type { ChartOptions } from 'chart.js'
import { Bar } from 'vue-chartjs'
import type { LsmCategoryDash } from '../../types/types'
import { dashboardGridColor, dashboardTickColor } from '../../services/chartSetup'

const props = withDefaults(
  defineProps<{
    categories: LsmCategoryDash[]
    animationDelay?: string
  }>(),
  {
    animationDelay: '0s',
  },
)

const lsmBarData = computed(() => ({
  labels: props.categories.map((d) => d.category),
  datasets: [
    {
      label: 'Similaridade',
      data: props.categories.map((d) => d.similarity),
      backgroundColor: 'hsl(147, 67%, 60%)',
      borderRadius: 4,
      borderSkipped: false,
      barPercentage: 0.75,
      categoryPercentage: 0.65,
    },
  ],
}))

const lsmBarOptions = computed<ChartOptions<'bar'>>(
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
          ticks: { color: dashboardTickColor, font: { size: 10 }, maxRotation: 35, minRotation: 0 },
          border: { display: false },
        },
        y: {
          min: 0,
          max: 100,
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
      <div class="dashboard-card-head">
        <div class="dashboard-card-title">
          <i class="pi pi-book dashboard-card-title__icon text-secondary" aria-hidden="true"></i>
          <span>LSM por Categoria</span>
        </div>
        <p class="dashboard-card-desc">Media de similaridade linguistica por categoria em todos os matches</p>
      </div>
    </template>
    <template #content>
      <div class="dashboard-chart-wrap dashboard-chart-wrap--tall">
        <Bar :data="lsmBarData" :options="lsmBarOptions" />
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

.dashboard-card-head {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
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

.dashboard-card-desc {
  margin: 0;
  font-size: 0.75rem;
  color: var(--token-text-muted);
  line-height: 1.35;
  font-weight: 400;
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
