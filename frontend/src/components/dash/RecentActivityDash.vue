<script setup lang="ts">
import { computed } from 'vue'
import Card from 'primevue/card'
import type { RecentActivityDash } from '../../types/types'

const props = withDefaults(
  defineProps<{
    activity: RecentActivityDash[]
    animationDelay?: string
  }>(),
  {
    animationDelay: '0s',
  },
)

function formatRelative(iso: string | null) {
  if (!iso) return '-'
  const diff = Math.max(0, Date.now() - new Date(iso).getTime())
  const mins = Math.floor(diff / 60_000)
  if (mins < 1) return 'Agora'
  if (mins < 60) return `${mins} min`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs} h`
  return `${Math.floor(hrs / 24)} d`
}

function activityBadgeClass(score: number) {
  if (score >= 80) return 'dashboard-act-badge--high'
  if (score >= 60) return 'dashboard-act-badge--mid'
  return 'dashboard-act-badge--low'
}

const items = computed(() =>
  props.activity.map((item) => ({
    ...item,
    time: formatRelative(item.occurred_at),
  })),
)
</script>

<template>
  <Card class="dashboard-card dash-animate" :style="{ animationDelay }">
    <template #title>
      <div class="dashboard-card-title">
        <i class="pi pi-bolt dashboard-card-title__icon text-secondary" aria-hidden="true"></i>
        <span>Atividade Recente</span>
      </div>
    </template>
    <template #content>
      <div v-if="items.length" class="dashboard-activity">
        <div
          v-for="item in items"
          :key="`${item.conversation_id}-${item.action}-${item.occurred_at}`"
          class="dashboard-activity__item"
        >
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
          <span v-if="item.score != null" class="dashboard-activity__badge" :class="activityBadgeClass(item.score)">
            {{ item.score }}
          </span>
        </div>
      </div>
      <p v-else class="dashboard-empty">Nenhuma atividade recente.</p>
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
</style>
