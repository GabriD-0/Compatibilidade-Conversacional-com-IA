<script setup lang="ts">
import { computed } from 'vue'
import Dialog from 'primevue/dialog'
import type { ConversationAnalysis } from '../../types/types'

type AnalysisComponent = {
  key: string
  label: string
  description: string
  icon: string
  value: number
}

const props = defineProps<{
  modelValue: boolean
  analysis: ConversationAnalysis | null
  loading: boolean
  error: string | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const components = computed<AnalysisComponent[]>(() => {
  const aggregateComponents = props.analysis?.metrics.aggregate?.components
  if (!aggregateComponents) return []

  return [
    {
      key: 'lsm',
      label: 'LSM',
      description: 'Estilo linguistico',
      icon: 'pi pi-book',
      value: aggregateComponents.lsm,
    },
    {
      key: 'sentiment',
      label: 'Sentimento',
      description: 'Convergencia emocional',
      icon: 'pi pi-heart',
      value: aggregateComponents.sentiment,
    },
    {
      key: 'behavioral',
      label: 'Comportamento',
      description: 'Sinais de ritmo e equilibrio',
      icon: 'pi pi-users',
      value: aggregateComponents.behavioral,
    },
  ].filter((component): component is AnalysisComponent => typeof component.value === 'number')
})

const warnings = computed(() => props.analysis?.warnings ?? props.analysis?.metrics.warnings ?? [])

function classificationLabel(classification: string | null | undefined): string {
  if (classification === 'high') return 'Alta'
  if (classification === 'mid') return 'Media'
  if (classification === 'low') return 'Baixa'
  return 'Sem classificacao'
}

function scoreClass(score: number | null | undefined): 'high' | 'mid' | 'low' | null {
  if (score == null) return null
  if (score >= 80) return 'high'
  if (score >= 60) return 'mid'
  return 'low'
}

function formatScore(score: number): string {
  if (Number.isInteger(score)) return String(score)
  return score.toFixed(2).replace(/\.?0+$/, '')
}

function componentWidth(value: number): string {
  return `${Math.min(100, Math.max(0, value))}%`
}

function scoreStyle(score: number): Record<string, string> {
  const clamped = Math.min(100, Math.max(0, score))
  return { '--score-angle': `${clamped * 3.6}deg` }
}

function formatDateTime(iso: string | null): string {
  if (!iso) return 'Agora'
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(iso))
}
</script>

<template>
  <Dialog
    :visible="modelValue"
    modal
    class="analysis-modal"
    :pt="{ mask: { class: 'analysis-modal-mask' } }"
    :style="{ width: 'min(44rem, calc(100vw - 1.5rem))' }"
    @update:visible="emit('update:modelValue', $event)"
  >
    <template #header>
      <div class="analysis-modal__head">
        <div class="analysis-modal__icon" aria-hidden="true">
          <i :class="loading ? 'pi pi-spinner pi-spin' : 'pi pi-chart-bar'"></i>
        </div>
        <div class="analysis-modal__title">
          <span>Analise da conversa</span>
          <strong v-if="analysis">
            {{ formatScore(analysis.score) }}% &middot; {{ classificationLabel(analysis.classification) }}
          </strong>
          <strong v-else-if="loading">Analisando conversa</strong>
          <strong v-else>Sem analise disponivel</strong>
        </div>
        <span
          v-if="analysis"
          :class="['analysis-modal__status', `analysis-modal__status--${analysis.classification}`]"
        >
          {{ classificationLabel(analysis.classification) }}
        </span>
      </div>
    </template>

    <div class="analysis-modal__body" aria-live="polite">
      <div v-if="analysis" class="analysis-modal__hero">
        <div class="analysis-modal__score-card">
          <div
            :class="[
              'analysis-modal__score-ring',
              scoreClass(analysis.score) ? `analysis-modal__score-ring--${scoreClass(analysis.score)}` : '',
            ]"
            :style="scoreStyle(analysis.score)"
          >
            <div class="analysis-modal__score-core">
              <strong>{{ formatScore(analysis.score) }}%</strong>
              <span>score</span>
            </div>
          </div>
          <div class="analysis-modal__score-meta">
            <span>{{ analysis.message_count }} mensagens</span>
            <span>{{ formatDateTime(analysis.computed_at) }}</span>
          </div>
        </div>

        <div class="analysis-modal__summary-card">
          <span class="analysis-modal__eyebrow">Resumo</span>
          <p v-if="analysis.explanation.summary" class="analysis-modal__summary">
            {{ analysis.explanation.summary }}
          </p>
          <p v-else class="analysis-modal__summary analysis-modal__summary--muted">
            A analise foi calculada, mas nao retornou um resumo explicativo.
          </p>
        </div>
      </div>

      <div v-else-if="loading" class="analysis-modal__loading">
        <div class="analysis-modal__loading-ring" aria-hidden="true">
          <i class="pi pi-spinner pi-spin"></i>
        </div>
        <div>
          <strong>Calculando compatibilidade</strong>
          <p>Processando score, componentes e avisos da conversa.</p>
        </div>
      </div>

      <div v-if="error" class="analysis-modal__error">
        <i class="pi pi-info-circle" aria-hidden="true"></i>
        <span>{{ error }}</span>
      </div>

      <div v-if="components.length" class="analysis-modal__metrics">
        <div
          v-for="component in components"
          :key="component.key"
          class="analysis-modal__metric"
        >
          <div class="analysis-modal__metric-icon" aria-hidden="true">
            <i :class="component.icon"></i>
          </div>
          <div class="analysis-modal__metric-head">
            <div>
              <span>{{ component.label }}</span>
              <small>{{ component.description }}</small>
            </div>
            <strong>{{ formatScore(component.value) }}%</strong>
          </div>
          <div class="analysis-modal__track" aria-hidden="true">
            <span
              class="analysis-modal__fill"
              :style="{ width: componentWidth(component.value) }"
            ></span>
          </div>
        </div>
      </div>

      <ul v-if="warnings.length" class="analysis-modal__warnings">
        <li
          v-for="(warning, index) in warnings"
          :key="`${warning.code}-${warning.participant_id ?? index}`"
        >
          <i class="pi pi-exclamation-triangle" aria-hidden="true"></i>
          <span>{{ warning.message }}</span>
        </li>
      </ul>
    </div>
  </Dialog>
</template>

<style scoped>
:global(.analysis-modal.p-dialog) {
  overflow: hidden;
  background:
    linear-gradient(135deg, rgba(13, 43, 48, 0.98) 0%, rgba(21, 24, 43, 0.98) 48%, rgba(48, 19, 43, 0.97) 100%),
    #101923 !important;
  border: 1px solid rgba(111, 241, 186, 0.22);
  border-radius: 1.1rem;
  color: #f7f2ff;
  backdrop-filter: blur(28px);
  box-shadow:
    0 24px 64px rgba(0, 0, 0, 0.68),
    0 0 36px rgba(90, 219, 148, 0.08);
}

:global(.analysis-modal-mask.p-dialog-mask) {
  background:
    linear-gradient(135deg, rgba(5, 35, 40, 0.44) 0%, rgba(18, 18, 42, 0.42) 48%, rgba(48, 14, 42, 0.4) 100%) !important;
  backdrop-filter: blur(8px) saturate(110%);
}

:global(.analysis-modal .p-dialog-header) {
  background: rgba(8, 28, 34, 0.28) !important;
  color: #f7f2ff;
  border-bottom: 1px solid rgba(111, 241, 186, 0.13);
  padding: 1.05rem 1.25rem;
}

:global(.analysis-modal .p-dialog-content) {
  background: rgba(9, 24, 35, 0.1) !important;
  color: inherit;
  padding: 1.1rem 1.25rem 1.2rem;
}

:global(.analysis-modal .p-dialog-footer) {
  background: rgba(8, 28, 34, 0.24) !important;
  border-top: 1px solid rgba(111, 241, 186, 0.1);
  padding: 0.85rem 1.25rem;
}

:global(.analysis-modal .p-dialog-header-icons) {
  align-self: flex-start;
}

:global(.analysis-modal .p-dialog-close-button) {
  color: rgba(240, 235, 255, 0.68);
}

:global(.analysis-modal .p-dialog-close-button:hover) {
  color: #f0ebff;
  background: rgba(255, 255, 255, 0.07);
}

.analysis-modal__head {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  min-width: 0;
  width: 100%;
}

.analysis-modal__icon {
  width: 2.4rem;
  height: 2.4rem;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border-radius: 0.75rem;
  color: #5adb94;
  background: linear-gradient(135deg, rgba(90, 219, 148, 0.16), rgba(11, 161, 140, 0.08));
  border: 1px solid rgba(90, 219, 148, 0.26);
  box-shadow: 0 0 18px rgba(90, 219, 148, 0.08);
}

.analysis-modal__title {
  min-width: 0;
  display: grid;
  gap: 0.16rem;
  flex: 1;
}

.analysis-modal__title span {
  font-size: 0.66rem;
  font-weight: 800;
  text-transform: uppercase;
  color: rgba(195, 178, 228, 0.56);
}

.analysis-modal__title strong {
  color: #f0ebff;
  font-size: 0.98rem;
  line-height: 1.25;
}

.analysis-modal__status {
  padding: 0.24rem 0.65rem;
  border-radius: 999px;
  font-size: 0.68rem;
  font-weight: 800;
}

.analysis-modal__status--high {
  color: #5adb94;
  background: rgba(90, 219, 148, 0.12);
  border: 1px solid rgba(90, 219, 148, 0.25);
}

.analysis-modal__status--mid {
  color: #fbbf24;
  background: rgba(251, 191, 36, 0.1);
  border: 1px solid rgba(251, 191, 36, 0.23);
}

.analysis-modal__status--low {
  color: #f87171;
  background: rgba(248, 113, 113, 0.1);
  border: 1px solid rgba(248, 113, 113, 0.23);
}

.analysis-modal__body {
  display: grid;
  gap: 1.05rem;
}

.analysis-modal__hero {
  display: grid;
  grid-template-columns: minmax(9rem, 0.72fr) minmax(0, 1.28fr);
  gap: 1rem;
}

.analysis-modal__score-card,
.analysis-modal__summary-card,
.analysis-modal__metric {
  border-radius: 0.75rem;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.075), rgba(255, 255, 255, 0.035)),
    rgba(12, 36, 44, 0.22);
  border: 1px solid rgba(255, 255, 255, 0.095);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.045),
    0 10px 28px rgba(4, 12, 18, 0.16);
}

.analysis-modal__score-card {
  display: grid;
  justify-items: center;
  align-content: center;
  gap: 0.75rem;
  padding: 1rem 0.85rem;
}

.analysis-modal__score-ring {
  --score-angle: 0deg;
  --score-color: #5adb94;
  width: 7.25rem;
  height: 7.25rem;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background:
    conic-gradient(var(--score-color) var(--score-angle), rgba(255, 255, 255, 0.08) 0),
    rgba(255, 255, 255, 0.04);
  box-shadow: 0 0 28px rgba(90, 219, 148, 0.09);
}

.analysis-modal__score-ring--mid {
  --score-color: #fbbf24;
  box-shadow: 0 0 28px rgba(251, 191, 36, 0.07);
}

.analysis-modal__score-ring--low {
  --score-color: #f87171;
  box-shadow: 0 0 28px rgba(248, 113, 113, 0.07);
}

.analysis-modal__score-core {
  width: calc(100% - 0.82rem);
  height: calc(100% - 0.82rem);
  display: grid;
  place-items: center;
  align-content: center;
  gap: 0.2rem;
  border-radius: 50%;
  background: linear-gradient(145deg, rgba(14, 38, 45, 0.98), rgba(31, 22, 45, 0.98));
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.analysis-modal__score-core strong {
  color: #f0ebff;
  font-size: 1.62rem;
  line-height: 1;
}

.analysis-modal__score-core span {
  color: rgba(195, 178, 228, 0.62);
  font-size: 0.66rem;
  font-weight: 800;
  text-transform: uppercase;
}

.analysis-modal__score-meta {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.35rem 0.55rem;
  color: rgba(195, 178, 228, 0.58);
  font-size: 0.7rem;
}

.analysis-modal__summary-card {
  display: grid;
  align-content: center;
  gap: 0.45rem;
  padding: 1rem;
}

.analysis-modal__eyebrow {
  color: rgba(90, 219, 148, 0.86);
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
}

.analysis-modal__summary,
.analysis-modal__state,
.analysis-modal__loading p {
  margin: 0;
  font-size: 0.86rem;
  line-height: 1.5;
}

.analysis-modal__summary,
.analysis-modal__state {
  color: rgba(240, 235, 255, 0.75);
}

.analysis-modal__summary--muted {
  color: rgba(195, 178, 228, 0.58);
}

.analysis-modal__loading,
.analysis-modal__error {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-height: 5rem;
  padding: 0.9rem 1rem;
  border-radius: 0.75rem;
}

.analysis-modal__loading {
  background: rgba(90, 219, 148, 0.07);
  border: 1px solid rgba(90, 219, 148, 0.15);
}

.analysis-modal__loading-ring {
  width: 2.5rem;
  height: 2.5rem;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border-radius: 50%;
  color: #5adb94;
  background: rgba(90, 219, 148, 0.1);
}

.analysis-modal__loading strong {
  display: block;
  margin-bottom: 0.14rem;
  color: #f0ebff;
  font-size: 0.9rem;
}

.analysis-modal__error {
  min-height: auto;
  color: #fca5a5;
  background: rgba(248, 113, 113, 0.08);
  border: 1px solid rgba(248, 113, 113, 0.18);
  font-size: 0.82rem;
  line-height: 1.4;
}

.analysis-modal__error .pi {
  flex-shrink: 0;
}

.analysis-modal__metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.7rem;
}

.analysis-modal__metric {
  min-width: 0;
  display: grid;
  gap: 0.65rem;
  padding: 0.85rem;
}

.analysis-modal__metric-icon {
  width: 2rem;
  height: 2rem;
  display: grid;
  place-items: center;
  border-radius: 0.6rem;
  color: #5adb94;
  background: rgba(90, 219, 148, 0.09);
  border: 1px solid rgba(90, 219, 148, 0.14);
}

.analysis-modal__metric-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.55rem;
}

.analysis-modal__metric-head span {
  display: block;
  color: rgba(195, 178, 228, 0.72);
  font-size: 0.78rem;
  font-weight: 700;
}

.analysis-modal__metric-head small {
  display: block;
  margin-top: 0.12rem;
  color: rgba(195, 178, 228, 0.48);
  font-size: 0.66rem;
  line-height: 1.25;
}

.analysis-modal__metric-head strong {
  color: rgba(240, 235, 255, 0.9);
  font-size: 0.82rem;
  flex-shrink: 0;
}

.analysis-modal__track {
  height: 0.44rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.07);
  overflow: hidden;
}

.analysis-modal__fill {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #5adb94, #0ba18c);
}

.analysis-modal__warnings {
  list-style: none;
  margin: 0;
  padding: 0.85rem;
  display: grid;
  gap: 0.42rem;
  border-radius: 0.75rem;
  background: rgba(251, 191, 36, 0.07);
  border: 1px solid rgba(251, 191, 36, 0.15);
}

.analysis-modal__warnings li {
  display: flex;
  align-items: flex-start;
  gap: 0.4rem;
  color: rgba(251, 191, 36, 0.9);
  font-size: 0.76rem;
  line-height: 1.4;
}

.analysis-modal__warnings .pi {
  flex-shrink: 0;
  margin-top: 0.08rem;
  font-size: 0.7rem;
}

@media (max-width: 720px) {
  .analysis-modal__hero,
  .analysis-modal__metrics {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 520px) {
  :global(.analysis-modal .p-dialog-header),
  :global(.analysis-modal .p-dialog-content),
  :global(.analysis-modal .p-dialog-footer) {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .analysis-modal__head {
    align-items: flex-start;
  }

  .analysis-modal__status {
    display: none;
  }

  .analysis-modal__score-ring {
    width: 6.4rem;
    height: 6.4rem;
  }
}
</style>
