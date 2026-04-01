<script setup lang="ts">
import Card from 'primevue/card'
import {
  ArcElement,
  BarElement,
  BubbleController,
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  RadialLinearScale,
  Title,
  Tooltip,
  type ChartOptions,
} from 'chart.js'
import { computed } from 'vue'
import { Bar, Bubble, Doughnut, Line, Radar } from 'vue-chartjs'
import { RouterLink } from 'vue-router'

ChartJS.register(
  ArcElement,
  BarElement,
  BubbleController,
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
)

const tickColor = 'rgba(255, 255, 255, 0.5)'
const gridColor = 'rgba(54, 137, 134, 0.15)'

const weeklyScores = [
  { day: 'Seg', score: 72, conversations: 12 },
  { day: 'Ter', score: 78, conversations: 15 },
  { day: 'Qua', score: 65, conversations: 9 },
  { day: 'Qui', score: 84, conversations: 18 },
  { day: 'Sex', score: 91, conversations: 22 },
  { day: 'Sáb', score: 88, conversations: 14 },
  { day: 'Dom', score: 76, conversations: 8 },
]

const radarData = [
  { metric: 'LSM', value: 82, fullMark: 100 },
  { metric: 'Emoção', value: 74, fullMark: 100 },
  { metric: 'Comportamento', value: 91, fullMark: 100 },
  { metric: 'Engajamento', value: 68, fullMark: 100 },
  { metric: 'Reciprocidade', value: 85, fullMark: 100 },
  { metric: 'Fluidez', value: 77, fullMark: 100 },
]

const distributionData = [
  { range: '0-20', count: 2 },
  { range: '21-40', count: 5 },
  { range: '41-60', count: 12 },
  { range: '61-80', count: 28 },
  { range: '81-100', count: 18 },
]

const pieData = [
  { name: 'Alta (80+)', value: 18, color: 'hsl(147, 67%, 60%)' },
  { name: 'Média (50-79)', value: 32, color: 'hsl(171, 85%, 36%)' },
  { name: 'Baixa (<50)', value: 7, color: 'hsl(330, 96%, 28%)' },
]

const topPairs = [
  { a: 'Eduardo', b: 'Fernanda', score: 94, trend: 'up' as const },
  { a: 'Ana', b: 'Bruno', score: 87, trend: 'up' as const },
  { a: 'Carlos', b: 'Diana', score: 62, trend: 'down' as const },
  { a: 'Gabriel', b: 'Helena', score: 45, trend: 'down' as const },
]

const recentActivity = [
  { pair: 'Ana & Bruno', action: 'Nova análise', score: 87, time: '2 min' },
  { pair: 'Eduardo & Fernanda', action: 'Score atualizado', score: 94, time: '15 min' },
  { pair: 'Carlos & Diana', action: 'Nova mensagem', score: 62, time: '32 min' },
  { pair: 'Igor & Julia', action: 'Conversa iniciada', score: null as number | null, time: '1h' },
]

/** Polaridade simulada por mensagem (mock) */
const emotionalConvergenceData = [
  { msg: 1, personA: 0.15, personB: -0.05 },
  { msg: 2, personA: 0.35, personB: 0.1 },
  { msg: 3, personA: 0.2, personB: 0.25 },
  { msg: 4, personA: 0.45, personB: 0.4 },
  { msg: 5, personA: 0.55, personB: 0.35 },
  { msg: 6, personA: 0.5, personB: 0.55 },
  { msg: 7, personA: 0.65, personB: 0.6 },
  { msg: 8, personA: 0.7, personB: 0.68 },
  { msg: 9, personA: 0.75, personB: 0.72 },
  { msg: 10, personA: 0.82, personB: 0.78 },
  { msg: 11, personA: 0.78, personB: 0.85 },
  { msg: 12, personA: 0.88, personB: 0.82 },
]

const lsmCategoryData = [
  { category: 'Pronomes', valueA: 82, valueB: 76 },
  { category: 'Artigos', valueA: 71, valueB: 74 },
  { category: 'Preposições', valueA: 88, valueB: 79 },
  { category: 'Conjunções', valueA: 69, valueB: 73 },
  { category: 'Auxiliares', valueA: 77, valueB: 81 },
  { category: 'Advérbios', valueA: 64, valueB: 70 },
]

const behavioralData = [
  { pair: 'Ana & Bruno', latency: 1.5, balance: 88, msgLength: 142 },
  { pair: 'Eduardo & Fernanda', latency: 8, balance: 72, msgLength: 96 },
  { pair: 'Carlos & Diana', latency: 14, balance: 58, msgLength: 210 },
]

const scatterData = [
  { pair: 'A & B', lsm: 78, sentiment: 72, score: 87 },
  { pair: 'C & D', lsm: 62, sentiment: 55, score: 62 },
  { pair: 'E & F', lsm: 91, sentiment: 88, score: 94 },
  { pair: 'G & H', lsm: 44, sentiment: 38, score: 45 },
  { pair: 'I & J', lsm: 55, sentiment: 60, score: 58 },
  { pair: 'K & L', lsm: 83, sentiment: 79, score: 81 },
]

function scatterPointColor(score: number) {
  if (score >= 80) return 'hsl(147, 67%, 60%)'
  if (score >= 50) return 'hsl(171, 85%, 36%)'
  return 'hsl(330, 96%, 28%)'
}

function scatterPointFill(score: number) {
  if (score >= 80) return 'rgba(90, 219, 148, 0.65)'
  if (score >= 50) return 'rgba(11, 161, 140, 0.65)'
  return 'rgba(138, 3, 77, 0.65)'
}

function bubbleRadiusFromScore(score: number) {
  return 6 + (score / 100) * 18
}

const stats = [
  { label: 'Score Médio', value: '78.2', icon: 'pi pi-chart-line', change: '+4.3%', up: true },
  { label: 'Conversas', value: '57', icon: 'pi pi-comments', change: '+12', up: true },
  { label: 'Pares Ativos', value: '14', icon: 'pi pi-users', change: '+2', up: true },
  { label: 'Análises Hoje', value: '23', icon: 'pi pi-bolt', change: '-3', up: false },
]

const convColor = 'hsl(171, 85%, 42%)'

const lineData = computed(() => ({
  labels: weeklyScores.map((d) => d.day),
  datasets: [
    {
      label: 'Score',
      data: weeklyScores.map((d) => d.score),
      yAxisID: 'y',
      borderColor: 'hsl(147, 67%, 60%)',
      backgroundColor: 'rgba(90, 219, 148, 0.2)',
      fill: true,
      tension: 0.35,
      borderWidth: 2,
      pointRadius: 3,
      pointBackgroundColor: 'hsl(147, 67%, 60%)',
      order: 2,
    },
    {
      label: 'Conversas',
      data: weeklyScores.map((d) => d.conversations),
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
            color: tickColor,
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
          grid: { color: gridColor, drawBorder: false },
          ticks: { color: tickColor, font: { size: 12 } },
          border: { display: false },
        },
        y: {
          id: 'y',
          type: 'linear',
          position: 'left',
          min: 0,
          max: 100,
          grid: { color: gridColor, drawBorder: false },
          ticks: { color: tickColor, font: { size: 12 } },
          border: { display: false },
        },
        y1: {
          id: 'y1',
          type: 'linear',
          position: 'right',
          min: 0,
          suggestedMax: 28,
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

const radarChartData = computed(() => ({
  labels: radarData.map((r) => r.metric),
  datasets: [
    {
      label: 'Valor',
      data: radarData.map((r) => r.value),
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
          angleLines: { color: gridColor },
          grid: { color: gridColor },
          pointLabels: {
            color: tickColor,
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

const barData = computed(() => ({
  labels: distributionData.map((d) => d.range),
  datasets: [
    {
      label: 'Quantidade',
      data: distributionData.map((d) => d.count),
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
          ticks: { color: tickColor, font: { size: 11 } },
          border: { display: false },
        },
        y: {
          grid: { color: gridColor, drawBorder: false },
          ticks: { color: tickColor, font: { size: 11 } },
          border: { display: false },
        },
      },
    }) as ChartOptions<'bar'>,
)

const doughnutData = computed(() => ({
  labels: pieData.map((p) => p.name),
  datasets: [
    {
      data: pieData.map((p) => p.value),
      backgroundColor: pieData.map((p) => p.color),
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

const emotionalLineData = computed(() => ({
  labels: emotionalConvergenceData.map((d) => `M${d.msg}`),
  datasets: [
    {
      label: 'Pessoa A',
      data: emotionalConvergenceData.map((d) => d.personA),
      borderColor: 'hsl(147, 67%, 60%)',
      backgroundColor: 'transparent',
      tension: 0.35,
      borderWidth: 2,
      pointRadius: 3,
      pointBackgroundColor: 'hsl(147, 67%, 60%)',
    },
    {
      label: 'Pessoa B',
      data: emotionalConvergenceData.map((d) => d.personB),
      borderColor: 'hsl(330, 96%, 28%)',
      backgroundColor: 'transparent',
      borderDash: [5, 5],
      tension: 0.35,
      borderWidth: 2,
      pointRadius: 3,
      pointBackgroundColor: 'hsl(330, 96%, 28%)',
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
          grid: { color: gridColor, drawBorder: false },
          ticks: { color: tickColor, font: { size: 11 }, maxRotation: 0 },
          border: { display: false },
        },
        y: {
          min: -1,
          max: 1,
          grid: { color: gridColor, drawBorder: false },
          ticks: { color: tickColor, font: { size: 11 } },
          border: { display: false },
        },
      },
    }) as ChartOptions<'line'>,
)

const lsmBarData = computed(() => ({
  labels: lsmCategoryData.map((d) => d.category),
  datasets: [
    {
      label: 'Participante A',
      data: lsmCategoryData.map((d) => d.valueA),
      backgroundColor: 'hsl(147, 67%, 60%)',
      borderRadius: 4,
      borderSkipped: false,
      barPercentage: 0.75,
      categoryPercentage: 0.65,
    },
    {
      label: 'Participante B',
      data: lsmCategoryData.map((d) => d.valueB),
      backgroundColor: 'hsl(330, 96%, 28%)',
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
          grid: { display: false, drawBorder: false },
          ticks: { color: tickColor, font: { size: 10 }, maxRotation: 35, minRotation: 0 },
          border: { display: false },
        },
        y: {
          min: 0,
          max: 100,
          grid: { color: gridColor, drawBorder: false },
          ticks: { color: tickColor, font: { size: 11 } },
          border: { display: false },
        },
      },
    }) as ChartOptions<'bar'>,
)

const bubbleChartData = computed(() => ({
  datasets: [
    {
      label: 'Pares',
      data: scatterData.map((d) => ({
        x: d.lsm,
        y: d.sentiment,
        r: bubbleRadiusFromScore(d.score),
      })),
      backgroundColor: scatterData.map((d) => scatterPointFill(d.score)),
      borderColor: scatterData.map((d) => scatterPointColor(d.score)),
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
              const i = ctx.dataIndex
              const row = scatterData[i]
              if (!row) return ''
              return `${row.pair} · LSM ${row.lsm} · Sent. ${row.sentiment} · Score ${row.score}`
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
          grid: { color: gridColor, drawBorder: false },
          ticks: { color: tickColor, font: { size: 11 } },
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
          grid: { color: gridColor, drawBorder: false },
          ticks: { color: tickColor, font: { size: 11 } },
          border: { display: false },
        },
      },
    }) as ChartOptions<'bubble'>,
)

function latencyClass(latency: number) {
  if (latency <= 2) return 'text-primary'
  if (latency <= 10) return 'text-secondary'
  return 'text-accent'
}

function balanceBarClass(balance: number) {
  if (balance >= 80) return 'dashboard-behav-bar--high'
  if (balance >= 60) return 'dashboard-behav-bar--mid'
  return 'dashboard-behav-bar--low'
}

function scoreClass(score: number) {
  if (score >= 80) return 'dash-pair-score--high'
  if (score >= 50) return 'dash-pair-score--mid'
  return 'dash-pair-score--low'
}

function activityBadgeClass(score: number) {
  if (score >= 80) return 'dash-act-badge--high'
  if (score >= 50) return 'dash-act-badge--mid'
  return 'dash-act-badge--low'
}
</script>

<template>
  <div class="dashboard-page">
    <div class="dashboard-page__glows" aria-hidden="true">
      <div class="dashboard-page__glow dashboard-page__glow--a" />
      <div class="dashboard-page__glow dashboard-page__glow--b" />
      <div class="dashboard-page__glow dashboard-page__glow--c" />
    </div>

    <nav class="dashboard-page__nav">
      <div class="dashboard-page__brand">
        <div class="dashboard-page__brand-mark">
          <span class="dashboard-page__brand-dot" />
        </div>
        <span class="dashboard-page__brand-name">ConversaIA</span>
      </div>
      <div class="dashboard-page__nav-links">
        <RouterLink to="/home" class="dashboard-page__link" active-class="dashboard-page__link--active">
          <i class="pi pi-home" aria-hidden="true"></i>
          Home
        </RouterLink>
        <RouterLink to="/chat" class="dashboard-page__link" active-class="dashboard-page__link--active">
          <i class="pi pi-comment" aria-hidden="true"></i>
          Chat
        </RouterLink>
        <RouterLink to="/dashboard" class="dashboard-page__link" active-class="dashboard-page__link--active">
          <i class="pi pi-chart-bar" aria-hidden="true"></i>
          Dashboard
        </RouterLink>
      </div>
    </nav>

    <main class="dashboard-page__main">
      <header class="dashboard-page__header dash-animate" style="animation-delay: 0s">
        <h1 class="dashboard-page__title">
          Dashboard de <span class="text-primary">Compatibilidade</span>
        </h1>
        <p class="dashboard-page__subtitle">Visão geral das análises de compatibilidade conversacional</p>
      </header>

      <div class="dashboard-page__stats">
        <Card
          v-for="(stat, i) in stats"
          :key="stat.label"
          class="dashboard-card dash-animate"
          :style="{ animationDelay: `${(i + 1) * 0.06}s` }"
        >
          <template #content>
            <div class="dashboard-stat">
              <div class="dashboard-stat__top">
                <div class="dashboard-stat__icon-wrap">
                  <i :class="[stat.icon, 'dashboard-stat__icon']" aria-hidden="true"></i>
                </div>
                <span
                  class="dashboard-stat__delta"
                  :class="stat.up ? 'text-primary' : 'text-accent'"
                >
                  <i
                    :class="stat.up ? 'pi pi-arrow-up-right' : 'pi pi-arrow-down-right'"
                    class="dashboard-stat__delta-ico"
                    aria-hidden="true"
                  ></i>
                  {{ stat.change }}
                </span>
              </div>
              <div class="dashboard-stat__value">{{ stat.value }}</div>
              <div class="dashboard-stat__label">{{ stat.label }}</div>
            </div>
          </template>
        </Card>
      </div>

      <div class="dashboard-page__row dashboard-page__row--charts">
        <Card class="dashboard-card dashboard-card--wide dash-animate" style="animation-delay: 0.35s">
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

        <Card class="dashboard-card dash-animate" style="animation-delay: 0.42s">
          <template #title>
            <div class="dashboard-card-title">
              <i class="pi pi-bolt dashboard-card-title__icon text-secondary" aria-hidden="true"></i>
              <span>Perfil Médio</span>
            </div>
          </template>
          <template #content>
            <div class="dashboard-chart-wrap dashboard-chart-wrap--tall">
              <Radar :data="radarChartData" :options="radarOptions" />
            </div>
          </template>
        </Card>
      </div>

      <div class="dashboard-page__row dashboard-page__row--charts">
        <Card class="dashboard-card dash-animate" style="animation-delay: 0.5s">
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

        <Card class="dashboard-card dash-animate" style="animation-delay: 0.56s">
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

        <Card class="dashboard-card dash-animate" style="animation-delay: 0.62s">
          <template #title>
            <div class="dashboard-card-title">
              <i class="pi pi-users dashboard-card-title__icon text-primary" aria-hidden="true"></i>
              <span>Top Pares</span>
            </div>
          </template>
          <template #content>
            <ul class="dashboard-top-pairs">
              <li v-for="(pair, i) in topPairs" :key="`${pair.a}-${pair.b}`" class="dashboard-top-pairs__item">
                <div class="dashboard-top-pairs__left">
                  <span class="dashboard-top-pairs__rank">#{{ i + 1 }}</span>
                  <span class="dashboard-top-pairs__names">{{ pair.a }} &amp; {{ pair.b }}</span>
                </div>
                <div class="dashboard-top-pairs__right">
                  <span class="dashboard-pair-score" :class="scoreClass(pair.score)">{{ pair.score }}</span>
                  <i
                    v-if="pair.trend === 'up'"
                    class="pi pi-arrow-up-right text-primary dashboard-top-pairs__trend"
                    aria-hidden="true"
                  ></i>
                  <i v-else class="pi pi-arrow-down-right text-accent dashboard-top-pairs__trend" aria-hidden="true"></i>
                </div>
              </li>
            </ul>
          </template>
        </Card>
      </div>

      <div class="dashboard-page__row dashboard-page__row--half">
        <Card class="dashboard-card dash-animate" style="animation-delay: 0.64s">
          <template #title>
            <div class="dashboard-card-head">
              <div class="dashboard-card-title">
                <i class="pi pi-heart dashboard-card-title__icon text-accent" aria-hidden="true"></i>
                <span>Convergência Emocional</span>
              </div>
              <p class="dashboard-card-desc">Polaridade de sentimento ao longo das mensagens</p>
            </div>
          </template>
          <template #content>
            <div class="dashboard-chart-wrap dashboard-chart-wrap--tall">
              <Line :data="emotionalLineData" :options="emotionalLineOptions" />
            </div>
          </template>
        </Card>

        <Card class="dashboard-card dash-animate" style="animation-delay: 0.7s">
          <template #title>
            <div class="dashboard-card-head">
              <div class="dashboard-card-title">
                <i class="pi pi-book dashboard-card-title__icon text-secondary" aria-hidden="true"></i>
                <span>LSM por Categoria</span>
              </div>
              <p class="dashboard-card-desc">Similaridade de estilo linguístico por tipo de palavra-função</p>
            </div>
          </template>
          <template #content>
            <div class="dashboard-chart-wrap dashboard-chart-wrap--tall">
              <Bar :data="lsmBarData" :options="lsmBarOptions" />
            </div>
          </template>
        </Card>
      </div>

      <div class="dashboard-page__row dashboard-page__row--half">
        <Card class="dashboard-card dash-animate" style="animation-delay: 0.76s">
          <template #title>
            <div class="dashboard-card-head">
              <div class="dashboard-card-title">
                <i class="pi pi-clock dashboard-card-title__icon text-secondary" aria-hidden="true"></i>
                <span>Sinais Comportamentais</span>
              </div>
              <p class="dashboard-card-desc">
                Latência de resposta, equilíbrio de turnos e tamanho médio por par
              </p>
            </div>
          </template>
          <template #content>
            <div class="dashboard-behav">
              <div v-for="(item, i) in behavioralData" :key="i" class="dashboard-behav__block">
                <div class="dashboard-behav__pair">{{ item.pair }}</div>
                <div class="dashboard-behav__grid">
                  <div>
                    <div class="dashboard-behav__label">
                      <i class="pi pi-clock dashboard-behav__mini" aria-hidden="true"></i>
                      Latência
                    </div>
                    <div class="dashboard-behav__mono font-mono text-sm font-bold" :class="latencyClass(item.latency)">
                      {{ item.latency }}min
                    </div>
                  </div>
                  <div>
                    <div class="dashboard-behav__label">
                      <i class="pi pi-arrows-h dashboard-behav__mini" aria-hidden="true"></i>
                      Equilíbrio
                    </div>
                    <div class="dashboard-behav__balance">
                      <div class="dashboard-behav__track">
                        <div
                          class="dashboard-behav__fill"
                          :class="balanceBarClass(item.balance)"
                          :style="{ width: `${item.balance}%` }"
                        />
                      </div>
                      <span class="dashboard-behav__mono font-mono text-xs">{{ item.balance }}%</span>
                    </div>
                  </div>
                  <div>
                    <div class="dashboard-behav__label">
                      <i class="pi pi-align-left dashboard-behav__mini" aria-hidden="true"></i>
                      Tam. Médio
                    </div>
                    <div class="dashboard-behav__mono dashboard-behav__value-muted font-mono text-sm font-bold">
                      {{ item.msgLength }} chars
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </Card>

        <Card class="dashboard-card dash-animate" style="animation-delay: 0.82s">
          <template #title>
            <div class="dashboard-card-head">
              <div class="dashboard-card-title">
                <i class="pi pi-chart-line dashboard-card-title__icon text-primary" aria-hidden="true"></i>
                <span>LSM vs Sentimento</span>
              </div>
              <p class="dashboard-card-desc">Correlação entre estilo linguístico e convergência emocional</p>
            </div>
          </template>
          <template #content>
            <div class="dashboard-chart-wrap dashboard-chart-wrap--scatter">
              <Bubble :data="bubbleChartData" :options="bubbleChartOptions" />
            </div>
            <div class="dashboard-scatter-legend">
              <span v-for="d in scatterData" :key="d.pair" class="dashboard-scatter-legend__item font-mono">
                {{ d.pair }} ({{ d.score }})
              </span>
            </div>
          </template>
        </Card>
      </div>

      <Card class="dashboard-card dash-animate" style="animation-delay: 0.88s">
        <template #title>
          <div class="dashboard-card-title">
            <i class="pi pi-bolt dashboard-card-title__icon text-secondary" aria-hidden="true"></i>
            <span>Atividade Recente</span>
          </div>
        </template>
        <template #content>
          <div class="dashboard-activity">
            <div v-for="(item, i) in recentActivity" :key="i" class="dashboard-activity__item">
              <div class="dashboard-activity__icon-wrap">
                <i class="pi pi-comments text-primary" aria-hidden="true"></i>
              </div>
              <div class="dashboard-activity__body">
                <div class="dashboard-activity__pair">{{ item.pair }}</div>
                <div class="dashboard-activity__meta">
                  <span>{{ item.action }}</span>
                  <span aria-hidden="true">·</span>
                  <span>{{ item.time }}</span>
                </div>
              </div>
              <span
                v-if="item.score != null"
                class="dashboard-activity__badge"
                :class="activityBadgeClass(item.score)"
              >
                {{ item.score }}
              </span>
            </div>
          </div>
        </template>
      </Card>
    </main>
  </div>
</template>

<style scoped>
.dashboard-page {
  position: relative;
  min-height: 100%;
  overflow-x: hidden;
  color: var(--token-text);
  background: var(--token-bg-page);
}

.dashboard-page__glows {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.dashboard-page__glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.06;
}

.dashboard-page__glow--a {
  top: -15%;
  left: -10%;
  width: 45%;
  height: 45%;
  background: var(--color-secondary);
}

.dashboard-page__glow--b {
  top: 40%;
  right: -8%;
  width: 30%;
  height: 30%;
  opacity: 0.04;
  filter: blur(100px);
  background: var(--color-accent);
}

.dashboard-page__glow--c {
  bottom: 10%;
  left: 30%;
  width: 20%;
  height: 20%;
  opacity: 0.05;
  filter: blur(90px);
  background: var(--color-primary);
}

.dashboard-page__nav {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.25rem 1.5rem 0;
}

.dashboard-page__brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dashboard-page__brand-mark {
  width: 2rem;
  height: 2rem;
  border-radius: 0.5rem;
  background: color-mix(in srgb, var(--color-primary) 20%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
}

.dashboard-page__brand-dot {
  width: 0.65rem;
  height: 0.65rem;
  border-radius: 50%;
  background: var(--color-primary);
  box-shadow: 0 0 12px var(--color-primary);
  animation: dash-pulse 2.4s ease-in-out infinite;
}

@keyframes dash-pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.55;
  }
}

.dashboard-page__brand-name {
  font-weight: 700;
  font-size: 1.125rem;
  letter-spacing: -0.02em;
}

.dashboard-page__nav-links {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  flex-wrap: wrap;
}

.dashboard-page__link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.85rem;
  border-radius: 999px;
  font-size: 0.875rem;
  text-decoration: none;
  color: var(--token-text-muted);
  transition:
    color 0.2s,
    background-color 0.2s;
}

.dashboard-page__link:hover {
  color: var(--token-text);
  background: color-mix(in srgb, var(--token-bg-surface) 50%, transparent);
}

.dashboard-page__link--active {
  background: color-mix(in srgb, var(--color-primary) 15%, transparent);
  color: var(--color-primary);
  font-weight: 600;
}

.dashboard-page__main {
  position: relative;
  z-index: 1;
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem 1.5rem 3rem;
}

.dashboard-page__header {
  margin-bottom: 2rem;
}

.dashboard-page__title {
  margin: 0 0 0.5rem;
  font-size: clamp(1.65rem, 4vw, 2.25rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.2;
}

.dashboard-page__subtitle {
  margin: 0;
  font-size: 0.95rem;
  color: var(--token-text-muted);
}

.dashboard-page__stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

@media (min-width: 1024px) {
  .dashboard-page__stats {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

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

.dashboard-stat__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.dashboard-stat__icon-wrap {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 0.5rem;
  background: color-mix(in srgb, var(--color-primary) 10%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
}

.dashboard-stat__icon {
  font-size: 1rem;
  color: var(--color-primary);
}

.dashboard-stat__delta {
  display: inline-flex;
  align-items: center;
  gap: 0.15rem;
  font-size: 0.75rem;
  font-family: ui-monospace, monospace;
  font-weight: 600;
}

.dashboard-stat__delta-ico {
  font-size: 0.7rem;
}

.dashboard-stat__value {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.dashboard-stat__label {
  font-size: 0.75rem;
  color: var(--token-text-muted);
  margin-top: 0.15rem;
}

.dashboard-page__row {
  display: grid;
  gap: 1rem;
  margin-bottom: 1rem;
}

.dashboard-page__row--charts {
  grid-template-columns: 1fr;
}

@media (min-width: 1024px) {
  .dashboard-page__row--charts {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.dashboard-page__row--half {
  grid-template-columns: 1fr;
}

@media (min-width: 1024px) {
  .dashboard-page__row--half {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.dashboard-card-head {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
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

.dashboard-chart-wrap--mid {
  height: 220px;
}

.dashboard-chart-wrap--pie {
  height: 180px;
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

.dashboard-behav {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.dashboard-behav__block {
  padding: 0.75rem;
  border-radius: 0.5rem;
  background: color-mix(in srgb, var(--token-bg-page) 30%, transparent);
  border: 1px solid color-mix(in srgb, var(--token-border) 20%, transparent);
}

.dashboard-behav__pair {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.dashboard-behav__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
}

@media (max-width: 640px) {
  .dashboard-behav__grid {
    grid-template-columns: 1fr;
  }
}

.dashboard-behav__label {
  font-size: 0.625rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--token-text-muted);
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.dashboard-behav__mini {
  font-size: 0.65rem;
  opacity: 0.85;
}

.dashboard-behav__value-muted {
  color: color-mix(in srgb, var(--token-text) 80%, transparent);
}

.dashboard-behav__balance {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.dashboard-behav__track {
  flex: 1;
  min-width: 0;
  height: 0.35rem;
  border-radius: 999px;
  background: color-mix(in srgb, var(--token-text-muted) 20%, transparent);
  overflow: hidden;
}

.dashboard-behav__fill {
  height: 100%;
  border-radius: 999px;
}

.dashboard-behav-bar--high {
  background: var(--color-primary);
}

.dashboard-behav-bar--mid {
  background: var(--color-secondary);
}

.dashboard-behav-bar--low {
  background: var(--color-accent);
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

.dashboard-top-pairs {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.dashboard-top-pairs__item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.6rem 0.65rem;
  border-radius: 0.5rem;
  background: color-mix(in srgb, var(--token-bg-page) 40%, transparent);
  border: 1px solid color-mix(in srgb, var(--token-border) 30%, transparent);
}

.dashboard-top-pairs__left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 0;
}

.dashboard-top-pairs__rank {
  font-size: 0.7rem;
  font-family: ui-monospace, monospace;
  color: var(--token-text-muted);
  width: 1.25rem;
}

.dashboard-top-pairs__names {
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dashboard-top-pairs__right {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  flex-shrink: 0;
}

.dashboard-pair-score {
  font-size: 0.875rem;
  font-weight: 700;
  font-family: ui-monospace, monospace;
}

.dashboard-pair-score--high {
  color: var(--color-primary);
}

.dashboard-pair-score--mid {
  color: var(--color-secondary);
}

.dashboard-pair-score--low {
  color: var(--color-accent);
}

.dashboard-top-pairs__trend {
  font-size: 0.85rem;
}

.dashboard-activity {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.65rem;
}

@media (min-width: 768px) {
  .dashboard-activity {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (min-width: 1024px) {
  .dashboard-activity {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

.dashboard-activity__item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  background: color-mix(in srgb, var(--token-bg-page) 30%, transparent);
  border: 1px solid color-mix(in srgb, var(--token-border) 20%, transparent);
}

.dashboard-activity__icon-wrap {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: color-mix(in srgb, var(--color-primary) 10%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.dashboard-activity__body {
  min-width: 0;
  flex: 1;
}

.dashboard-activity__pair {
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dashboard-activity__meta {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.75rem;
  color: var(--token-text-muted);
}

.dashboard-activity__badge {
  font-size: 0.7rem;
  font-weight: 700;
  font-family: ui-monospace, monospace;
  padding: 0.15rem 0.45rem;
  border-radius: 999px;
  flex-shrink: 0;
}

.dashboard-act-badge--high {
  background: color-mix(in srgb, var(--color-primary) 10%, transparent);
  color: var(--color-primary);
}

.dashboard-act-badge--mid {
  background: color-mix(in srgb, var(--color-secondary) 10%, transparent);
  color: var(--color-secondary);
}

.dashboard-act-badge--low {
  background: color-mix(in srgb, var(--color-accent) 10%, transparent);
  color: var(--color-accent);
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

@media (prefers-color-scheme: light) {
  .dashboard-page__glow--a {
    opacity: 0.09;
  }

  .dashboard-page__glow--b {
    opacity: 0.06;
  }

  .dashboard-page__glow--c {
    opacity: 0.08;
  }
}
</style>
