<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import BehavioralSignsDash from '../components/dash/BehavioralSignsDash.vue'
import CategoryDistributionDash from '../components/dash/CategoryDistributionDash.vue'
import StatsDash from '../components/dash/StatsDash.vue'
import EmotionalConvergenceDash from '../components/dash/EmotionalConvergenceDash.vue'
import LsmCategoryDash from '../components/dash/LsmCategoryDash.vue'
import LsmSentimentDash from '../components/dash/LsmSentimentDash.vue'
import Loading from '../components/Loading.vue'
import ProfileDash from '../components/dash/ProfileDash.vue'
import RecentActivityDash from '../components/dash/RecentActivityDash.vue'
import ScoreDistributionDash from '../components/dash/ScoreDistributionDash.vue'
import TopPairsDash from '../components/dash/TopPairsDash.vue'
import WeeklyScoreDash from '../components/dash/WeeklyScoreDash.vue'
import { dashboardApi, extractApiError } from '../services/api'
import type { SummaryDash } from '../types/types'

const emptySummary: SummaryDash = {
  stats: {
    average_score: { value: null, delta: null },
    conversations: { value: 0, delta: 0 },
    analyzed_pairs: { value: 0, delta: 0 },
    analyses_today: { value: 0, delta: 0 },
  },
  weekly_scores: [],
  profile: [],
  score_distribution: [],
  classification_distribution: [],
  top_pairs: [],
  recent_activity: [],
  emotional_convergence: [],
  lsm_categories: [],
  behavioral_signs: [],
  scatter: [],
}

const dashboard = ref<SummaryDash | null>(null)
const loadingDashboard = ref(false)
const dashboardError = ref<string | null>(null)

const summary = computed(() => dashboard.value ?? emptySummary)

onMounted(loadDashboard)

async function loadDashboard() {
  loadingDashboard.value = true
  dashboardError.value = null

  try {
    dashboard.value = await dashboardApi.getSummary()
  } catch (err) {
    dashboardError.value = extractApiError(err)
  } finally {
    loadingDashboard.value = false
  }
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
    </nav>

    <main class="dashboard-page__main">
      <header class="dashboard-page__header dash-animate" style="animation-delay: 0s">
        <h1 class="dashboard-page__title">
          Dashboard de <span class="text-primary">Compatibilidade</span>
        </h1>
        <p class="dashboard-page__subtitle">Visão geral das análises de compatibilidade conversacional</p>
        <p v-if="dashboardError" class="dashboard-page__status dashboard-page__status--error">
          {{ dashboardError }}
        </p>
      </header>

      <Loading v-if="loadingDashboard" />

      <template v-else>
        <StatsDash :stats="summary.stats" />

        <div class="dashboard-page__row dashboard-page__row--charts">
          <WeeklyScoreDash :weekly-scores="summary.weekly_scores" animation-delay="0.35s" />
          <ProfileDash :profile="summary.profile" animation-delay="0.42s" />
        </div>

        <div class="dashboard-page__row dashboard-page__row--charts">
          <ScoreDistributionDash :distribution="summary.score_distribution" animation-delay="0.5s" />
          <CategoryDistributionDash :distribution="summary.classification_distribution" animation-delay="0.56s" />
          <TopPairsDash :pairs="summary.top_pairs" animation-delay="0.62s" />
        </div>

        <div class="dashboard-page__row dashboard-page__row--half">
          <EmotionalConvergenceDash :conversations="summary.emotional_convergence" animation-delay="0.64s" />
          <LsmCategoryDash :categories="summary.lsm_categories" animation-delay="0.7s" />
        </div>

        <div class="dashboard-page__row dashboard-page__row--half">
          <BehavioralSignsDash :signs="summary.behavioral_signs" animation-delay="0.76s" />
          <LsmSentimentDash :points="summary.scatter" animation-delay="0.82s" />
        </div>

        <RecentActivityDash :activity="summary.recent_activity" animation-delay="0.88s" />
      </template>
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
  letter-spacing: 0;
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
  font-size: 2.25rem;
  font-weight: 700;
  letter-spacing: 0;
  line-height: 1.2;
}

@media (max-width: 640px) {
  .dashboard-page__title {
    font-size: 1.65rem;
  }
}

.dashboard-page__subtitle {
  margin: 0;
  font-size: 0.95rem;
  color: var(--token-text-muted);
}

.dashboard-page__status {
  margin: 0.7rem 0 0;
  font-size: 0.8rem;
  color: var(--token-text-muted);
}

.dashboard-page__status--error {
  color: var(--color-accent);
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
