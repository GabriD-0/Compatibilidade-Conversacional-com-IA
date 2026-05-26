<script setup lang="ts">
import { computed } from 'vue'
import Card from 'primevue/card'
import type { BehavioralSignDash } from '../../types/types'

const props = withDefaults(
  defineProps<{
    signs: BehavioralSignDash[]
    animationDelay?: string
  }>(),
  {
    animationDelay: '0s',
  },
)

const behavioralData = computed(() =>
  props.signs.map((item) => ({
    pair: item.pair,
    latency: item.latency_minutes,
    balance: item.balance,
    msgLength: item.message_length_words,
  })),
)

function formatNumber(value: number | null, digits = 0) {
  if (value == null || Number.isNaN(value)) return '-'
  if (digits === 0) return String(Math.round(value))
  return value.toFixed(digits).replace(/\.?0+$/, '')
}

function latencyClass(latency: number | null) {
  if (latency == null) return ''
  if (latency <= 2) return 'text-primary'
  if (latency <= 10) return 'text-secondary'
  return 'text-accent'
}

function formatLatency(latency: number | null) {
  if (latency == null) return '-'
  return `${formatNumber(latency, Number.isInteger(latency) ? 0 : 1)}min`
}

function balanceBarClass(balance: number) {
  if (balance >= 80) return 'dashboard-behav-bar--high'
  if (balance >= 60) return 'dashboard-behav-bar--mid'
  return 'dashboard-behav-bar--low'
}
</script>

<template>
  <Card class="dashboard-card dash-animate" :style="{ animationDelay }">
    <template #title>
      <div class="dashboard-card-head">
        <div class="dashboard-card-title">
          <i class="pi pi-clock dashboard-card-title__icon text-secondary" aria-hidden="true"></i>
          <span>Sinais Comportamentais</span>
        </div>
        <p class="dashboard-card-desc">Latencia, equilibrio de turnos e tamanho medio por match</p>
      </div>
    </template>
    <template #content>
      <div v-if="behavioralData.length" class="dashboard-behav">
        <div v-for="(item, i) in behavioralData" :key="i" class="dashboard-behav__block">
          <div class="dashboard-behav__pair">{{ item.pair }}</div>
          <div class="dashboard-behav__grid">
            <div>
              <div class="dashboard-behav__label">
                <i class="pi pi-clock dashboard-behav__mini" aria-hidden="true"></i>
                Latência
              </div>
              <div class="dashboard-behav__mono font-mono text-sm font-bold" :class="latencyClass(item.latency)">
                {{ formatLatency(item.latency) }}
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
                {{ item.msgLength }} palavras
              </div>
            </div>
          </div>
        </div>
      </div>
      <p v-else class="dashboard-empty">Nenhuma analise comportamental disponivel.</p>
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

.dashboard-empty {
  margin: 0;
  padding: 1rem;
  border-radius: 0.5rem;
  color: var(--token-text-muted);
  background: color-mix(in srgb, var(--token-bg-page) 30%, transparent);
  border: 1px solid color-mix(in srgb, var(--token-border) 20%, transparent);
  font-size: 0.82rem;
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
  letter-spacing: 0;
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
