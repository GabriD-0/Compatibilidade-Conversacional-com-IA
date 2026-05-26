<template>
  <div class="dash-loading" role="status" aria-live="polite" aria-label="Carregando dashboards">
    <div class="dash-loading__panel">
      <span class="dash-loading__spinner" aria-hidden="true"></span>
      <span class="dash-loading__text">Carregando dashboards...</span>
    </div>
  </div>
</template>

<style scoped>
.dash-loading {
  min-height: calc(100vh - 14rem);
  display: grid;
  place-items: center;
  padding: 2rem 0 4rem;
}

.dash-loading__panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: var(--token-text-muted);
}

.dash-loading__spinner {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  border: 3px solid color-mix(in srgb, var(--token-border) 28%, transparent);
  border-top-color: var(--color-primary);
  box-shadow: 0 0 28px color-mix(in srgb, var(--color-primary) 24%, transparent);
  animation: dash-loading-spin 0.85s linear infinite;
}

.dash-loading__text {
  font-size: 0.9rem;
  font-weight: 600;
}

@keyframes dash-loading-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
