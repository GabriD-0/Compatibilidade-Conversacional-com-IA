<script setup lang="ts">
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'
import { nextTick, ref, watch } from 'vue'

type Sender = 'A' | 'B'

type Message = {
  id: string
  sender: Sender
  text: string
  time: string
}

type Conversation = {
  id: string
  participantA: string
  participantB: string
  avatarColorA: string
  avatarColorB: string
  score: number | null
  messages: Message[]
}

const props = defineProps<{
  conversation: Conversation
}>()

const emit = defineEmits<{
  back: []
}>()

const messages = ref<Message[]>([...props.conversation.messages])
const input = ref('')
const activeSender = ref<Sender>('A')
const scrollRef = ref<HTMLDivElement | null>(null)

function scrollToEnd() {
  nextTick(() => {
    if (scrollRef.value) {
      scrollRef.value.scrollTop = scrollRef.value.scrollHeight
    }
  })
}

watch(
  () => props.conversation.id,
  () => {
    messages.value = [...props.conversation.messages]
    input.value = ''
    activeSender.value = 'A'
    scrollToEnd()
  },
  { immediate: true },
)

watch(
  () => messages.value.length,
  () => {
    scrollToEnd()
  },
)

function getCurrentName(sender: Sender): string {
  return sender === 'A' ? props.conversation.participantA : props.conversation.participantB
}

function getCurrentAvatar(sender: Sender): string {
  return sender === 'A' ? props.conversation.avatarColorA : props.conversation.avatarColorB
}

function formatNow(): string {
  const now = new Date()
  return `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
}

function handleSend() {
  const text = input.value.trim()
  if (!text) return

  messages.value.push({
    id: `${props.conversation.id}-${Date.now()}`,
    sender: activeSender.value,
    text,
    time: formatNow(),
  })
  input.value = ''
}
</script>

<template>
  <div class="chat-view">
    <header class="chat-view__header">
      <div class="chat-view__left">
        <Button
          icon="pi pi-arrow-left"
          severity="secondary"
          text
          rounded
          aria-label="Voltar"
          @click="emit('back')"
        />
        <div class="chat-view__participants">
          <strong>{{ conversation.participantA }} &amp; {{ conversation.participantB }}</strong>
          <small>{{ messages.length }} mensagens</small>
        </div>
      </div>

      <Tag v-if="conversation.score !== null" :value="`Score ${conversation.score}`" severity="success" />
    </header>

    <div ref="scrollRef" class="chat-view__messages">
      <div
        v-for="message in messages"
        :key="message.id"
        class="chat-view__row"
        :class="{ 'chat-view__row--right': message.sender === 'B' }"
      >
        <div class="chat-view__avatar" :class="getCurrentAvatar(message.sender)">
          {{ getCurrentName(message.sender).charAt(0) }}
        </div>
        <div class="chat-view__bubble" :class="{ 'chat-view__bubble--right': message.sender === 'B' }">
          <p>{{ message.text }}</p>
          <small>{{ message.time }}</small>
        </div>
      </div>
    </div>

    <footer class="chat-view__footer">
      <div class="chat-view__sender">
        <small>Enviando como:</small>
        <div class="chat-view__sender-actions">
          <Button
            :label="conversation.participantA"
            :outlined="activeSender !== 'A'"
            size="small"
            @click="activeSender = 'A'"
          />
          <Button
            :label="conversation.participantB"
            :outlined="activeSender !== 'B'"
            size="small"
            @click="activeSender = 'B'"
          />
        </div>
      </div>

      <div class="chat-view__input-row">
        <InputText
          v-model="input"
          class="chat-view__input"
          :placeholder="`Escrever como ${getCurrentName(activeSender)}...`"
          @keydown.enter="handleSend"
        />
        <Button icon="pi pi-send" aria-label="Enviar" :disabled="!input.trim()" @click="handleSend" />
      </div>
    </footer>
  </div>
</template>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid var(--token-border);
  border-radius: 0.75rem;
  background: var(--token-bg-surface);
}

.chat-view__header,
.chat-view__footer {
  padding: 0.9rem;
  border-bottom: 1px solid var(--token-border);
}

.chat-view__footer {
  border-bottom: 0;
  border-top: 1px solid var(--token-border);
}

.chat-view__left {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.chat-view__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-view__participants strong {
  font-size: 0.92rem;
}

.chat-view__participants small,
.chat-view__sender small {
  display: block;
  color: var(--token-text-muted);
}

.chat-view__messages {
  flex: 1;
  overflow-y: auto;
  display: grid;
  gap: 0.7rem;
  padding: 1rem;
}

.chat-view__row {
  display: flex;
  align-items: flex-start;
  gap: 0.45rem;
}

.chat-view__row--right {
  justify-content: flex-end;
  flex-direction: row-reverse;
}

.chat-view__avatar {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 999px;
  display: grid;
  place-items: center;
  font-size: 0.7rem;
  font-weight: 700;
  color: #fff;
}

.chat-view__bubble {
  max-width: 72%;
  border: 1px solid var(--token-border);
  border-radius: 0.9rem;
  padding: 0.55rem 0.75rem;
  background: color-mix(in srgb, var(--token-bg-page) 12%, var(--token-bg-surface));
}

.chat-view__bubble--right {
  background: color-mix(in srgb, var(--color-primary) 14%, var(--token-bg-surface));
}

.chat-view__bubble p {
  margin: 0;
}

.chat-view__bubble small {
  display: block;
  text-align: right;
  color: var(--token-text-muted);
  margin-top: 0.25rem;
}

.chat-view__sender {
  margin-bottom: 0.55rem;
}

.chat-view__sender-actions {
  display: flex;
  gap: 0.45rem;
  margin-top: 0.4rem;
}

.chat-view__input-row {
  display: flex;
  gap: 0.55rem;
}

.chat-view__input {
  flex: 1;
}
</style>
