<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

const props = withDefaults(
  defineProps<{
    score: number
    size?: number
  }>(),
  {
    size: 180,
  },
)

const radius = computed(() => (props.size - 16) / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const targetOffset = computed(() => circumference.value - (props.score / 100) * circumference.value)
const animatedOffset = ref(circumference.value)

onMounted(() => {
  requestAnimationFrame(() => {
    animatedOffset.value = targetOffset.value
  })
})
</script>

<template>
  <div class="ring" :style="{ width: `${size}px`, height: `${size}px` }">
    <svg :width="size" :height="size" class="ring__svg">
      <circle :cx="size / 2" :cy="size / 2" :r="radius" fill="none" class="ring__track" />
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        class="ring__progress"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="animatedOffset"
      />
    </svg>

    <div class="ring__label">
      <strong>{{ score }}</strong>
      <small>score</small>
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
  stroke: color-mix(in srgb, var(--color-tertiary) 35%, transparent);
  stroke-width: 6;
}

.ring__progress {
  stroke: var(--color-primary);
  stroke-width: 6;
  stroke-linecap: round;
  transition: stroke-dashoffset 1.5s ease;
}

.ring__label {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  text-align: center;
}

.ring__label strong {
  display: block;
  line-height: 1;
  font-size: clamp(2rem, 6vw, 2.5rem);
  color: var(--color-primary);
}

.ring__label small {
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--token-text-muted);
}
</style>
