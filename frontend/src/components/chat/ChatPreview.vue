<script setup lang="ts">
type PreviewMessage = {
  sender: 'A' | 'B'
  text: string
  time: string
}

const messages: PreviewMessage[] = [
  { sender: 'A', text: 'Achei muito interessante essa abordagem!', time: '14:32' },
  { sender: 'B', text: 'Sim! A gente pensa muito parecido nisso.', time: '14:33' },
  { sender: 'A', text: 'Exatamente, e uma sintonia natural.', time: '14:33' },
  { sender: 'B', text: 'Vamos explorar mais essa ideia juntos?', time: '14:34' },
]
</script>

<template>
  <div class="preview">
    <div
      v-for="(message, index) in messages"
      :key="`${message.sender}-${index}`"
      class="preview__row flex"
      :class="message.sender === 'B' ? 'justify-end' : 'justify-start'"
    >
      <div
        class="max-w-[80%] px-4 py-2.5 rounded-2xl text-sm text-foreground bg-muted/20 shadow-sm"
        :class="message.sender === 'B' ? 'rounded-br-sm preview__bubble--right' : 'rounded-bl-sm preview__bubble'"
      >
        <p class="m-0 leading-snug">{{ message.text }}</p>
        <small class="mt-1 block text-right text-xs text-muted">{{ message.time }}</small>
      </div>
    </div>
  </div>
</template>

<style scoped>
.preview {
  display: grid;
  gap: 0.65rem;
  margin-top: 0.5rem;
}

.preview__bubble {
  background: rgba(255, 255, 255, 0.06);
}

.preview__bubble--right {
  background: rgba(11, 161, 140, 0.18);
}
</style>
