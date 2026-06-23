<script setup lang="ts">
import { computed } from 'vue'
import Card from 'primevue/card'
import type { ChartOptions } from 'chart.js'
import { Bubble } from 'vue-chartjs'
import type { ScatterPointDash } from '../../types/types'
import { dashboardGridColor, dashboardTickColor } from '../../services/chartSetup'
import InfoTooltipDash from './InfoTooltipDash.vue'

const props = withDefaults(
  defineProps<{
    points: ScatterPointDash[]
    animationDelay?: string
  }>(),
  {
    animationDelay: '0s',
  },
)

function scatterPointColor(score: number) {
  if (score >= 80) return 'hsl(147, 67%, 60%)'
  if (score >= 60) return 'hsl(171, 85%, 36%)'
  return 'hsl(330, 96%, 28%)'
}

function scatterPointFill(score: number) {
  if (score >= 80) return 'rgba(90, 219, 148, 0.65)'
  if (score >= 60) return 'rgba(11, 161, 140, 0.65)'
  return 'rgba(138, 3, 77, 0.65)'
}

function bubbleRadiusFromScore(score: number) {
  return 6 + (Math.max(0, Math.min(100, score)) / 100) * 18
}

const bubbleChartData = computed(() => ({
  datasets: [
    {
      label: 'Pares',
      data: props.points.map((d) => ({
        x: d.lsm,
        y: d.sentiment,
        r: bubbleRadiusFromScore(d.score),
      })),
      backgroundColor: props.points.map((d) => scatterPointFill(d.score)),
      borderColor: props.points.map((d) => scatterPointColor(d.score)),
      borderWidth: 1,
    },
  ],
}))

const bubbleChartOptions = computed<ChartOptions<'bubble'>>(
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
          callbacks: {
            label(ctx) {
              const row = props.points[ctx.dataIndex]
              if (!row) return ''
              return `${row.pair} - LSM ${row.lsm} - Sent. ${row.sentiment} - Score ${row.score}`
            },
          },
        },
      },
      scales: {
        x: {
          type: 'linear',
          min: 0,
          max: 100,
          title: {
            display: true,
            text: 'LSM Score',
            color: 'rgba(255, 255, 255, 0.4)',
            font: { size: 10 },
            padding: { top: 8 },
          },
          grid: { color: dashboardGridColor, drawBorder: false },
          ticks: { color: dashboardTickColor, font: { size: 11 } },
          border: { display: false },
        },
        y: {
          type: 'linear',
          min: 0,
          max: 100,
          title: {
            display: true,
            text: 'Sentimento',
            color: 'rgba(255, 255, 255, 0.4)',
            font: { size: 10 },
          },
          grid: { color: dashboardGridColor, drawBorder: false },
          ticks: { color: dashboardTickColor, font: { size: 11 } },
          border: { display: false },
        },
      },
    }) as ChartOptions<'bubble'>,
)
</script>

<template>
  <Card class="dashboard-card dash-animate" :style="{ animationDelay }">
    <template #title>
      <div class="dashboard-card-head">
        <div class="dashboard-card-title">
          <i class="pi pi-chart-line dashboard-card-title__icon text-primary" aria-hidden="true"></i>
          <span>LSM vs Sentimento</span>
          <InfoTooltipDash text="Cada bolha representa um par: a posição horizontal e o LSM, a vertical e o sentimento. O tamanho e a cor da bolha representam o score de compatibilidade; são exibidos os 12 maiores scores." />
        </div>
        <p class="dashboard-card-desc">Correlação entre estilo linguístico e convergência emocional</p>
      </div>
    </template>
    <template #content>
      <div class="dashboard-chart-wrap dashboard-chart-wrap--scatter">
        <Bubble :data="bubbleChartData" :options="bubbleChartOptions" />
      </div>
      <div class="dashboard-scatter-legend">
        <span v-for="d in points" :key="d.pair" class="dashboard-scatter-legend__item font-mono">
          {{ d.pair }} ({{ d.score }})
        </span>
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

.dashboard-chart-wrap--scatter {
  height: 300px;
}

.dashboard-scatter-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem 0.85rem;
  justify-content: center;
  margin-top: 0.5rem;
}

.dashboard-scatter-legend__item {
  font-size: 0.625rem;
  color: var(--token-text-muted);
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
