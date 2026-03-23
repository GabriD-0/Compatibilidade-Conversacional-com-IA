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
      class="preview__row"
      :class="{ 'preview__row--right': message.sender === 'B' }"
    >
      <div class="preview__bubble" :class="{ 'preview__bubble--b': message.sender === 'B' }">
        <p>{{ message.text }}</p>
        <small>{{ message.time }}</small>
      </div>
    </div>
  </div>
</template>

<style scoped>
.preview {
  display: grid;
  gap: 1.1rem;
  margin-top: 0.6rem;
}

.preview__row {
  display: flex;
}

.preview__row--right {
  justify-content: flex-end;
}

.preview__bubble {
  max-width: 84%;
  min-width: 36%;
  padding: 0.78rem 0.92rem;
  border-radius: 0.9rem;
  background: color-mix(in srgb, #3e495f 80%, transparent);
}

.preview__bubble--b {
  background: color-mix(in srgb, #444c60 84%, transparent);
}

.preview__bubble p {
  margin: 0;
  font-size: 0.98rem;
}

.preview__bubble small {
  display: block;
  margin-top: 0.25rem;
  text-align: right;
  color: color-mix(in srgb, var(--token-text) 56%, transparent);
  font-size: 0.76rem;
}
</style>
