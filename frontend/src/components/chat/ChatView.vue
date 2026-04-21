<script setup lang="ts">
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
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
  analyze: []
}>()

const messages = ref<Message[]>([...props.conversation.messages])
const input = ref('')
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

function getAvatarClass(sender: Sender): string {
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
    sender: 'A',
    text,
    time: formatNow(),
  })
  input.value = ''
}

function onAnalyze() {
  emit('analyze')
}
</script>

<template>
  <div class="chat-view">
    <header class="chat-view__header">
      <div class="chat-view__left">
        <Button
          icon="pi pi-arrow-left"
          class="chat-view__back"
          text
          rounded
          aria-label="Voltar"
          @click="emit('back')"
        />
        <span :class="['chat-view__head-av', conversation.avatarColorB]" aria-hidden="true">
          {{ conversation.participantB.charAt(0) }}
        </span>
        <div class="chat-view__participants">
          <strong>{{ conversation.participantB }}</strong>
          <small>{{ messages.length }} mensagens</small>
        </div>
      </div>

      <div class="chat-view__header-right">
        <template v-if="conversation.score !== null">
          <i class="pi pi-chart-bar chat-view__score-ico" aria-hidden="true"></i>
          <span class="chat-view__score-num">{{ conversation.score }}</span>
        </template>
        <button type="button" class="chat-view__analyze" @click="onAnalyze">Analisar</button>
      </div>
    </header>

    <div ref="scrollRef" class="chat-view__messages">
      <div class="chat-view__messages-body">
        <div
          v-for="message in messages"
          :key="message.id"
          class="chat-view__row"
          :class="{ 'chat-view__row--right': message.sender === 'A' }"
        >
          <div v-if="message.sender === 'B'" class="chat-view__avatar" :class="getAvatarClass(message.sender)">
            {{ conversation.participantB.charAt(0) }}
          </div>

          <div class="chat-view__bubble" :class="{ 'chat-view__bubble--right': message.sender === 'A' }">
            <p>{{ message.text }}</p>
            <small>{{ message.time }}</small>
          </div>
        </div>
      </div>
    </div>

    <footer class="chat-view__footer">
      <div class="chat-view__footer-body">
      <div class="chat-view__input-row">
        <InputText
          v-model="input"
          class="chat-view__input"
          placeholder="Escrever uma mensagem..."
          @keydown.enter="handleSend"
        />
        <Button
          icon="pi pi-send"
          class="chat-view__send"
          rounded
          aria-label="Enviar"
          :disabled="!input.trim()"
          @click="handleSend"
        />
      </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.chat-view {
  --cv-panel: #231530;
  --cv-deep: #1a0d24;
  --cv-border: rgba(90, 219, 148, 0.22);
  --cv-accent: #5adb94;
  --cv-muted: rgba(255, 255, 255, 0.55);
  --cv-bubble-left: #2a1838;
  --cv-bubble-right: rgba(138, 3, 77, 0.35);
  --cv-input-bg: #150a1c;

  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid var(--cv-border);
  border-radius: 1.25rem;
  background: var(--cv-panel);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
  overflow: hidden;
}

.chat-view__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding: 0.85rem 1rem;
  border-bottom: 1px solid var(--cv-border);
  flex-shrink: 0;
}

.chat-view__left {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  min-width: 0;
}

.chat-view__back {
  color: var(--cv-muted) !important;
  flex-shrink: 0;
}

.chat-view__head-av {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 0.72rem;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.chat-view__participants {
  min-width: 0;
}

.chat-view__participants strong {
  display: block;
  font-size: 0.95rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.02em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-view__participants small {
  display: block;
  margin-top: 0.15rem;
  font-size: 0.78rem;
  color: var(--cv-muted);
}

.chat-view__header-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
  margin-left: auto;
}

.chat-view__score-ico {
  font-size: 1rem;
  color: var(--cv-accent);
  opacity: 0.9;
}

.chat-view__score-num {
  font-size: 0.95rem;
  font-weight: 700;
  color: #fff;
}

.chat-view__analyze {
  margin: 0;
  padding: 0.45rem 1rem;
  font-size: 0.82rem;
  font-weight: 700;
  font-family: inherit;
  color: #1a0d24;
  background: var(--cv-accent);
  border: none;
  border-radius: 999px;
  cursor: pointer;
  transition: filter 0.15s ease, transform 0.1s ease;
}

.chat-view__analyze:hover {
  filter: brightness(1.06);
}

.chat-view__analyze:active {
  transform: scale(0.98);
}

.chat-view__messages {
  flex: 1;
  overflow-y: auto;
  background: var(--cv-deep);
  padding: 1rem 1.1rem;
}

.chat-view__messages-body {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  margin: 1 auto;
  width: 100%;
}

.chat-view__row {
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  min-width: 0;
}

.chat-view__row--right {
  justify-content: flex;
  flex-direction: row-reverse;
}

.chat-view__avatar {
  width: 1.85rem;
  height: 1.85rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 0.72rem;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.chat-view__bubble {
  max-width: 78%;
  min-width: 0;
  border-radius: 1.35rem;
  padding: 0.65rem 0.95rem 0.5rem;
  background: var(--cv-bubble-left);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.chat-view__bubble--right {
  background: var(--cv-bubble-right);
  border-color: rgba(255, 255, 255, 0.08);
}

.chat-view__bubble p {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.45;
  color: rgba(255, 255, 255, 0.92);
  overflow-wrap: break-word;
  word-break: break-word;
}

.chat-view__bubble small {
  display: block;
  text-align: right;
  font-size: 0.68rem;
  color: var(--cv-muted);
  margin-top: 0.35rem;
}

.chat-view__footer {
  padding: 0.9rem 1.1rem 1rem;
  border-top: 1px solid var(--cv-border);
  background: var(--cv-panel);
  flex-shrink: 0;
}

.chat-view__footer-body {
  max-width: 48rem;
  margin: 0 auto;
  width: 100%;
}

.chat-view__input-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  min-width: 0;
}

.chat-view__input {
  flex: 1;
  min-width: 0;
  border-radius: 1.5rem !important;
  background: var(--cv-input-bg) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  color: #fff !important;
  padding: 0.75rem 1.15rem !important;
  font-size: 0.92rem !important;
}

.chat-view__input::placeholder {
  color: var(--cv-muted);
}

.chat-view__send {
  width: 2.85rem !important;
  height: 2.85rem !important;
  padding: 0 !important;
  flex-shrink: 0;
  background: var(--cv-accent) !important;
  border: none !important;
  color: #1a0d24 !important;
}

.chat-view__send:disabled {
  opacity: 0.45;
}

@media (prefers-color-scheme: light) {
  .chat-view {
    --cv-panel: #ffffff;
    --cv-deep: #f1f0f5;
    --cv-border: rgba(11, 161, 140, 0.2);
    --cv-muted: rgba(33, 53, 71, 0.62);
    --cv-bubble-left: #ede9f4;
    --cv-bubble-right: rgba(11, 161, 140, 0.18);
    --cv-input-bg: #f6f4fa;
  }

  .chat-view__participants strong {
    color: #1e1530;
  }

  .chat-view__score-num {
    color: #1e1530;
  }

  .chat-view__bubble p {
    color: #1e1530;
  }

  .chat-view__input {
    color: #1e1530 !important;
  }

  .chat-view__pill {
    color: var(--cv-muted);
  }

  .chat-view__pill--on {
    color: #0ba18c;
  }
}
</style>
