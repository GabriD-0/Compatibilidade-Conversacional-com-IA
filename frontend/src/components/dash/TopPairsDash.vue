<script setup lang="ts">
import Card from 'primevue/card'
import type { TopPairDash } from '../../types/types'

withDefaults(
  defineProps<{
    pairs: TopPairDash[]
    animationDelay?: string
  }>(),
  {
    animationDelay: '0s',
  },
)

function scoreClass(score: number) {
  if (score >= 80) return 'dashboard-pair-score--high'
  if (score >= 60) return 'dashboard-pair-score--mid'
  return 'dashboard-pair-score--low'
}

function matchName(pair: TopPairDash) {
  return pair.b || pair.a
}
</script>

<template>
  <Card class="dashboard-card dash-animate" :style="{ animationDelay }">
    <template #title>
      <div class="dashboard-card-title">
        <i class="pi pi-users dashboard-card-title__icon text-primary" aria-hidden="true"></i>
        <span>Top Pares</span>
      </div>
    </template>
    <template #content>
      <ul v-if="pairs.length" class="dashboard-top-pairs">
        <li v-for="(pair, i) in pairs" :key="`${pair.a}-${pair.b}`" class="dashboard-top-pairs__item">
          <div class="dashboard-top-pairs__left">
            <span class="dashboard-top-pairs__rank">#{{ i + 1 }}</span>
            <span class="dashboard-top-pairs__names">{{ matchName(pair) }}</span>
          </div>
          <div class="dashboard-top-pairs__right">
            <span class="dashboard-pair-score" :class="scoreClass(pair.score)">{{ pair.score }}</span>
            <i
              v-if="pair.trend === 'up'"
              class="pi pi-arrow-up-right text-primary dashboard-top-pairs__trend"
              aria-hidden="true"
            ></i>
            <i
              v-else-if="pair.trend === 'down'"
              class="pi pi-arrow-down-right text-accent dashboard-top-pairs__trend"
              aria-hidden="true"
            ></i>
            <i v-else class="pi pi-minus dashboard-top-pairs__trend" aria-hidden="true"></i>
          </div>
        </li>
      </ul>
      <p v-else class="dashboard-empty">Nenhuma analise disponivel.</p>
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

.dashboard-empty {
  margin: 0;
  padding: 1rem;
  border-radius: 0.5rem;
  color: var(--token-text-muted);
  background: color-mix(in srgb, var(--token-bg-page) 30%, transparent);
  border: 1px solid color-mix(in srgb, var(--token-border) 20%, transparent);
  font-size: 0.82rem;
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
