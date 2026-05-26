<script setup lang="ts">
import { computed } from 'vue'
import Card from 'primevue/card'
import type { StatsDash } from '../../types/types'

const props = defineProps<{
  stats: StatsDash
}>()

function formatNumber(value: number | null, digits = 0) {
  if (value == null || Number.isNaN(value)) return '-'
  if (digits === 0) return String(Math.round(value))
  return value.toFixed(digits).replace(/\.?0+$/, '')
}

function formatDelta(value: number | null, suffix = '') {
  if (value == null || Number.isNaN(value)) return '-'
  const sign = value > 0 ? '+' : ''
  const digits = Number.isInteger(value) ? 0 : 1
  return `${sign}${formatNumber(value, digits)}${suffix}`
}

const items = computed(() => [
  {
    label: 'Score Medio',
    value: formatNumber(props.stats.average_score.value, 1),
    icon: 'pi pi-chart-line',
    change: formatDelta(props.stats.average_score.delta, '%'),
    up: props.stats.average_score.delta == null || props.stats.average_score.delta >= 0,
    tone: 'score',
  },
  {
    label: 'Conversas',
    value: formatNumber(props.stats.conversations.value),
    icon: 'pi pi-comments',
    change: formatDelta(props.stats.conversations.delta),
    up: props.stats.conversations.delta == null || props.stats.conversations.delta >= 0,
    tone: 'chat',
  },
  {
    label: 'Pares Ativos',
    value: formatNumber(props.stats.active_pairs.value),
    icon: 'pi pi-users',
    change: formatDelta(props.stats.active_pairs.delta),
    up: props.stats.active_pairs.delta == null || props.stats.active_pairs.delta >= 0,
    tone: 'pairs',
  },
  {
    label: 'Analises Hoje',
    value: formatNumber(props.stats.analyses_today.value),
    icon: 'pi pi-bolt',
    change: formatDelta(props.stats.analyses_today.delta),
    up: props.stats.analyses_today.delta == null || props.stats.analyses_today.delta >= 0,
    tone: 'today',
  },
])
</script>

<template>
  <div class="dashboard-stats">
    <Card
      v-for="(stat, i) in items"
      :key="stat.label"
      class="dashboard-card dash-animate"
      :class="`dashboard-card--${stat.tone}`"
      :style="{ animationDelay: `${(i + 1) * 0.06}s` }"
    >
      <template #content>
        <div class="dashboard-stat">
          <div class="dashboard-stat__top">
            <div class="dashboard-stat__icon-wrap">
              <i :class="[stat.icon, 'dashboard-stat__icon']" aria-hidden="true"></i>
            </div>
            <span class="dashboard-stat__delta" :class="stat.up ? 'dashboard-stat__delta--up' : 'dashboard-stat__delta--down'">
              <i
                :class="stat.up ? 'pi pi-arrow-up-right' : 'pi pi-arrow-down-right'"
                class="dashboard-stat__delta-ico"
                aria-hidden="true"
              ></i>
              {{ stat.change }}
            </span>
          </div>
          <div class="dashboard-stat__main">
            <div class="dashboard-stat__label">{{ stat.label }}</div>
            <div class="dashboard-stat__value">{{ stat.value }}</div>
          </div>
          <div class="dashboard-stat__footer">
            <span class="dashboard-stat__caption">Periodo atual</span>
            <span class="dashboard-stat__trend" :class="stat.up ? 'dashboard-stat__trend--up' : 'dashboard-stat__trend--down'">
              {{ stat.up ? 'Em alta' : 'Em queda' }}
            </span>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<style scoped>
.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 13.5rem), 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

@media (min-width: 1024px) {
  .dashboard-stats {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

.dashboard-card {
  --stat-color: var(--color-primary);
  --stat-color-soft: color-mix(in srgb, var(--stat-color) 12%, transparent);
  position: relative;
  overflow: hidden;
  min-height: 10.25rem;
  background:
    linear-gradient(145deg, color-mix(in srgb, var(--stat-color) 8%, transparent), transparent 46%),
    color-mix(in srgb, var(--token-bg-surface) 58%, transparent) !important;
  backdrop-filter: blur(14px);
  border: 1px solid color-mix(in srgb, var(--token-border) 42%, transparent) !important;
  border-radius: 0.55rem;
  box-shadow: 0 16px 38px rgba(0, 0, 0, 0.16);
  transition:
    border-color 0.2s,
    box-shadow 0.2s,
    transform 0.2s;
}

.dashboard-card--chat {
  --stat-color: var(--color-secondary);
}

.dashboard-card--pairs {
  --stat-color: var(--color-tertiary);
}

.dashboard-card--today {
  --stat-color: var(--color-accent);
}

.dashboard-card::before {
  content: '';
  position: absolute;
  inset: 0 auto 0 0;
  width: 0.2rem;
  background: var(--stat-color);
  opacity: 0.85;
}

.dashboard-card :deep(.p-card-body) {
  height: 100%;
  padding: 1rem;
}

.dashboard-card :deep(.p-card-content) {
  height: 100%;
  padding: 0;
}

.dashboard-card:hover {
  transform: translateY(-2px);
  border-color: color-mix(in srgb, var(--stat-color) 42%, transparent) !important;
  box-shadow: 0 18px 44px rgba(0, 0, 0, 0.22);
}

.dashboard-stat {
  min-height: 8.25rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.9rem;
}

.dashboard-stat__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.dashboard-stat__icon-wrap {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  background: var(--stat-color-soft);
  border: 1px solid color-mix(in srgb, var(--stat-color) 24%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
}

.dashboard-stat__icon {
  font-size: 1.05rem;
  color: var(--stat-color);
}

.dashboard-stat__delta {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  max-width: 8rem;
  min-height: 1.65rem;
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-family: ui-monospace, monospace;
  font-weight: 600;
  background: color-mix(in srgb, currentColor 10%, transparent);
  white-space: nowrap;
}

.dashboard-stat__delta--up {
  color: var(--color-primary);
}

.dashboard-stat__delta--down {
  color: var(--color-accent);
}

.dashboard-stat__delta-ico {
  font-size: 0.7rem;
}

.dashboard-stat__main {
  display: grid;
  gap: 0.15rem;
}

.dashboard-stat__value {
  color: var(--token-text);
  font-size: 2rem;
  line-height: 1.05;
  font-weight: 800;
  letter-spacing: 0;
}

.dashboard-stat__label {
  order: -1;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--token-text-muted);
}

.dashboard-stat__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid color-mix(in srgb, var(--token-border) 18%, transparent);
}

.dashboard-stat__caption,
.dashboard-stat__trend {
  font-size: 0.72rem;
  line-height: 1.2;
}

.dashboard-stat__caption {
  color: color-mix(in srgb, var(--token-text-muted) 82%, transparent);
}

.dashboard-stat__trend {
  flex-shrink: 0;
  font-weight: 700;
}

.dashboard-stat__trend--up {
  color: var(--color-primary);
}

.dashboard-stat__trend--down {
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

@media (max-width: 520px) {
  .dashboard-card {
    min-height: 9.75rem;
  }

  .dashboard-card :deep(.p-card-body) {
    padding: 0.9rem;
  }

  .dashboard-stat__value {
    font-size: 1.75rem;
  }
}
</style>
