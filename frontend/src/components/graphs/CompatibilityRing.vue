<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useId } from 'vue'

const props = withDefaults(
  defineProps<{
    score: number
    size?: number
  }>(),
  {
    size: 180,
  },
)

const gradId = `ring-grad-${useId().replace(/[^a-zA-Z0-9_-]/g, '')}`

const strokeW = 8
const radius = computed(() => (props.size - strokeW - 12) / 2)

/** Offset normalizado (pathLength=100): 0 = anel cheio, 100 = vazio */
const targetOffset = computed(() => {
  const clamped = Math.min(100, Math.max(0, props.score))
  return 100 - clamped
})

const animatedOffset = ref(100)

onMounted(() => {
  requestAnimationFrame(() => {
    animatedOffset.value = targetOffset.value
  })
})

watch(targetOffset, (next) => {
  animatedOffset.value = next
})
</script>

<template>
  <div class="ring" :style="{ width: `${size}px`, height: `${size}px` }">
    <svg :width="size" :height="size" class="ring__svg" :aria-label="`Score ${score} por cento`">
      <defs>
        <linearGradient :id="gradId" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#5df2a5" />
          <stop offset="100%" stop-color="#5adb94" />
        </linearGradient>
      </defs>
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        class="ring__track"
        :stroke-width="strokeW"
      />
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        pathLength="100"
        class="ring__progress"
        :stroke-width="strokeW"
        :stroke="`url(#${gradId})`"
        stroke-dasharray="100"
        :stroke-dashoffset="animatedOffset"
      />
    </svg>

    <div class="ring__label">
      <strong>{{ score }}</strong>
      <span class="ring__score-word">score</span>
    </div>
  </div>
</template>

<style scoped>
.ring {
  position: relative;
}

.ring__svg {
  transform: rotate(-90deg);
}

.ring__track {
  stroke: color-mix(in srgb, var(--color-tertiary) 28%, #1a1520);
  opacity: 0.9;
}

.ring__progress {
  stroke-linecap: round;
  transition: stroke-dashoffset 1.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.ring__label {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.2rem;
  text-align: center;
  pointer-events: none;
}

.ring__label strong {
  display: block;
  line-height: 1;
  font-size: clamp(2.1rem, 5.5vw, 2.65rem);
  font-weight: 800;
  color: var(--token-text);
  letter-spacing: -0.03em;
}

.ring__score-word {
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: color-mix(in srgb, var(--token-text) 82%, transparent);
}
</style>
