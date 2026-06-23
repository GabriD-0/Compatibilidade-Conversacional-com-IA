<script setup lang="ts">
withDefaults(defineProps<{text: string, label?: string, position?: 'center' | 'start'}>(),
  {
    label: 'Mais informacoes',
    position: 'center',
  },
)
</script>

<template>
  <span class="dashboard-info-tooltip" :class="`dashboard-info-tooltip--${position}`">
    <button type="button" class="dashboard-info-tooltip__trigger" :aria-label="label">
      <i class="pi pi-info-circle" aria-hidden="true"></i>
    </button>
    <span class="dashboard-info-tooltip__content" role="tooltip">{{ text }}</span>
  </span>
</template>

<style scoped>
.dashboard-info-tooltip {
  position: relative;
  display: inline-flex;
  flex: 0 0 auto;
}

.dashboard-info-tooltip__trigger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.25rem;
  height: 1.25rem;
  padding: 0;
  border: 0;
  border-radius: 50%;
  color: var(--token-text-muted);
  background: transparent;
  cursor: help;
  font: inherit;
}

.dashboard-info-tooltip__trigger:hover,
.dashboard-info-tooltip__trigger:focus-visible {
  color: var(--color-primary);
  background: color-mix(in srgb, var(--color-primary) 12%, transparent);
  outline: none;
}

.dashboard-info-tooltip__content {
  position: absolute;
  top: calc(100% + 0.45rem);
  left: 50%;
  z-index: 10;
  width: min(18rem, calc(100vw - 2rem));
  padding: 0.65rem 0.75rem;
  border: 1px solid color-mix(in srgb, var(--token-border) 75%, transparent);
  border-radius: 0.45rem;
  color: var(--token-text);
  background: color-mix(in srgb, var(--token-bg-surface) 96%, #000);
  box-shadow: 0 0.75rem 1.75rem rgba(0, 0, 0, 0.24);
  font-size: 0.75rem;
  font-weight: 400;
  line-height: 1.4;
  opacity: 0;
  pointer-events: none;
  transform: translate(-50%, -0.25rem);
  transition: opacity 0.15s ease, transform 0.15s ease;
  visibility: hidden;
}

.dashboard-info-tooltip:hover .dashboard-info-tooltip__content,
.dashboard-info-tooltip:focus-within .dashboard-info-tooltip__content {
  opacity: 1;
  transform: translate(-50%, 0);
  visibility: visible;
}

.dashboard-info-tooltip--start .dashboard-info-tooltip__content {
  left: 0;
  transform: translate(0, -0.25rem);
}

.dashboard-info-tooltip--start:hover .dashboard-info-tooltip__content,
.dashboard-info-tooltip--start:focus-within .dashboard-info-tooltip__content {
  transform: translate(0, 0);
}
</style>
