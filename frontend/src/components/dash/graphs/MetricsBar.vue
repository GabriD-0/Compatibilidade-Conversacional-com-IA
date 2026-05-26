<script setup lang="ts">
import ProgressBar from 'primevue/progressbar'

type Metric = {
  label: string
  shortLabel: string
  value: number
}

const metrics: Metric[] = [
  { label: 'Estilo Linguistico', shortLabel: 'LSM', value: 82 },
  { label: 'Convergencia Emocional', shortLabel: 'EMO', value: 74 },
  { label: 'Sinais Comportamentais', shortLabel: 'BHV', value: 91 },
]
</script>

<template>
  <div class="metrics">
    <div v-for="metric in metrics" :key="metric.shortLabel" class="metrics__item">
      <div class="metrics__head">
        <span>{{ metric.label }}</span>
        <strong>{{ metric.value }}%</strong>
      </div>
      <ProgressBar :value="metric.value" :show-value="false" :class="`metrics__bar metrics__bar--${metric.shortLabel.toLowerCase()}`" />
    </div>
  </div>
</template>

<style scoped>
.metrics {
  display: grid;
  gap: 1rem;
}

.metrics__item {
  display: grid;
  gap: 0.5rem;
}

.metrics__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.metrics__head span {
  color: color-mix(in srgb, var(--token-text) 84%, transparent);
  font-size: 1.03rem;
}

.metrics__head strong {
  color: var(--token-text);
  font-size: 1.45rem;
  line-height: 1;
  letter-spacing: -0.02em;
}

.metrics :deep(.p-progressbar) {
  height: 0.43rem;
  border-radius: 999px;
  background: color-mix(in srgb, #273147 75%, transparent);
}

.metrics :deep(.p-progressbar-value) {
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
}

.metrics__bar--emo :deep(.p-progressbar-value) {
  background: linear-gradient(90deg, #10c3a6, #27b48f);
}

.metrics__bar--bhv :deep(.p-progressbar-value) {
  background: linear-gradient(90deg, #4bcad5, #38a0a8);
}
</style>
