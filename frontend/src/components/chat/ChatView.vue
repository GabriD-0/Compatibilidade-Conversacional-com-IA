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

const props = defineProps<{ conversation: Conversation }>()

const emit = defineEmits<{ back: []; analyze: [] }>()

const messages = ref<Message[]>([...props.conversation.messages])
const input = ref('')
const scrollRef = ref<HTMLDivElement | null>(null)

const AVATAR_GRADIENTS = [
  'linear-gradient(135deg, #5adb94, #0ba18c)',
  'linear-gradient(135deg, #c0345e, #6d0080)',
  'linear-gradient(135deg, #7c3aed, #4f46e5)',
  'linear-gradient(135deg, #0ea5e9, #0891b2)',
  'linear-gradient(135deg, #f59e0b, #ef4444)',
  'linear-gradient(135deg, #ec4899, #8b5cf6)',
]

function avatarGradient(name: string): string {
  return AVATAR_GRADIENTS[name.charCodeAt(0) % AVATAR_GRADIENTS.length]!
}

function scoreLabel(score: number | null): 'high' | 'mid' | 'low' | null {
  if (score === null) return null
  if (score >= 80) return 'high'
  if (score >= 60) return 'mid'
  return 'low'
}

function scrollToEnd() {
  nextTick(() => {
    if (scrollRef.value) scrollRef.value.scrollTop = scrollRef.value.scrollHeight
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

watch(() => messages.value.length, scrollToEnd)

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
</script>

<template>
  <div class="chat-view">
    <!-- Header -->
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
        <div class="chat-view__av-wrap">
          <span
            class="chat-view__head-av"
            :style="{ background: avatarGradient(conversation.participantB) }"
            aria-hidden="true"
          >{{ conversation.participantB.charAt(0) }}</span>
          <span class="chat-view__online-dot"></span>
        </div>
        <div class="chat-view__participants">
          <strong>{{ conversation.participantB }}</strong>
          <small>{{ messages.length }} mensagens · online</small>
        </div>
      </div>

      <div class="chat-view__header-right">
        <span
          v-if="conversation.score !== null"
          :class="['chat-view__score-badge', `chat-view__score-badge--${scoreLabel(conversation.score)}`]"
        >
          <i class="pi pi-chart-bar"></i> {{ conversation.score }}%
        </span>
        <button type="button" class="chat-view__analyze" @click="emit('analyze')">
          <i class="pi pi-sparkles"></i> Analisar
        </button>
      </div>
    </header>

    <!-- Messages -->
    <div ref="scrollRef" class="chat-view__messages">
      <div class="chat-view__messages-body">
        <div
          v-for="message in messages"
          :key="message.id"
          class="chat-view__row"
          :class="{ 'chat-view__row--right': message.sender === 'A' }"
        >
          <div
            v-if="message.sender === 'B'"
            class="chat-view__avatar"
            :style="{ background: avatarGradient(conversation.participantB) }"
          >{{ conversation.participantB.charAt(0) }}</div>

          <div
            class="chat-view__bubble"
            :class="message.sender === 'A' ? 'chat-view__bubble--sent' : 'chat-view__bubble--recv'"
          >
            <p>{{ message.text }}</p>
            <small>{{ message.time }}</small>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="chat-view__footer">
      <div class="chat-view__footer-body">
        <div class="chat-view__input-row">
          <button class="chat-view__attach" aria-label="Anexar arquivo" type="button">
            <i class="pi pi-paperclip"></i>
          </button>
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
  --cv-bg: #080114;
  --cv-surface: rgba(16, 3, 28, 0.93);
  --cv-border: rgba(90, 219, 148, 0.11);
  --cv-accent: #5adb94;
  --cv-magenta: #8a034d;
  --cv-muted: rgba(195, 178, 228, 0.5);
  --cv-text: #f0ebff;

  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid var(--cv-border);
  border-radius: 1.5rem;
  background: var(--cv-surface);
  backdrop-filter: blur(28px) saturate(160%);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.04),
    0 24px 64px rgba(0, 0, 0, 0.65),
    0 0 48px rgba(90, 219, 148, 0.04);
  overflow: hidden;
}

/* ── Header ── */
.chat-view__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding: 0.9rem 1.1rem;
  background: rgba(10, 2, 20, 0.65);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--cv-border);
  flex-shrink: 0;
}

.chat-view__left {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  min-width: 0;
}

.chat-view__back {
  color: var(--cv-muted) !important;
  flex-shrink: 0;
  transition: color 0.15s !important;
}

.chat-view__back:hover {
  color: var(--cv-text) !important;
}

/* Avatar */
.chat-view__av-wrap {
  position: relative;
  flex-shrink: 0;
}

.chat-view__head-av {
  width: 2.45rem;
  height: 2.45rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 0.84rem;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.45);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.45);
}

.chat-view__online-dot {
  position: absolute;
  bottom: 1px;
  right: 1px;
  width: 0.58rem;
  height: 0.58rem;
  border-radius: 50%;
  background: var(--cv-accent);
  border: 2px solid rgba(10, 2, 20, 0.95);
  box-shadow: 0 0 8px rgba(90, 219, 148, 0.6);
}

/* Participants info */
.chat-view__participants { min-width: 0; }

.chat-view__participants strong {
  display: block;
  font-size: 0.93rem;
  font-weight: 700;
  color: var(--cv-text);
  letter-spacing: -0.02em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-view__participants small {
  display: block;
  margin-top: 0.1rem;
  font-size: 0.7rem;
  color: var(--cv-muted);
}

.chat-view__header-right {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-shrink: 0;
  margin-left: auto;
}

/* Score badge */
.chat-view__score-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.3rem 0.8rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
}

.chat-view__score-badge .pi { font-size: 0.68rem; }

.chat-view__score-badge--high {
  background: rgba(90, 219, 148, 0.13);
  color: #5adb94;
  border: 1px solid rgba(90, 219, 148, 0.28);
  box-shadow: 0 0 14px rgba(90, 219, 148, 0.1);
}

.chat-view__score-badge--mid {
  background: rgba(251, 191, 36, 0.11);
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.24);
}

.chat-view__score-badge--low {
  background: rgba(248, 113, 113, 0.11);
  color: #f87171;
  border: 1px solid rgba(248, 113, 113, 0.24);
}

/* Analyze button */
.chat-view__analyze {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.44rem 1.05rem;
  font-size: 0.8rem;
  font-weight: 700;
  font-family: inherit;
  color: #060010;
  background: linear-gradient(135deg, #5adb94, #0ba18c);
  border: none;
  border-radius: 999px;
  cursor: pointer;
  transition: filter 0.15s ease, transform 0.12s ease, box-shadow 0.15s ease;
  box-shadow: 0 4px 18px rgba(90, 219, 148, 0.28);
}

.chat-view__analyze .pi { font-size: 0.72rem; }

.chat-view__analyze:hover {
  filter: brightness(1.08);
  transform: translateY(-1px);
  box-shadow: 0 7px 24px rgba(90, 219, 148, 0.38);
}

.chat-view__analyze:active {
  transform: scale(0.97);
}

/* ── Messages area ── */
.chat-view__messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.35rem 1.1rem;
  scrollbar-width: thin;
  scrollbar-color: rgba(90, 219, 148, 0.1) transparent;

  background-color: #080114;
  background-image:
    radial-gradient(ellipse 45% 38% at 18% 22%, rgba(138, 3, 77, 0.09)  0%, transparent 65%),
    radial-gradient(ellipse 38% 32% at 82% 78%, rgba(90, 219, 148, 0.07) 0%, transparent 65%),
    radial-gradient(ellipse 30% 25% at 60% 40%, rgba(60, 0, 90, 0.15)    0%, transparent 65%);
}

.chat-view__messages-body {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  width: 100%;
  max-width: 54rem;
  margin: 0 auto;
}

.chat-view__row {
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  min-width: 0;
}

.chat-view__row--right {
  flex-direction: row-reverse;
}

.chat-view__avatar {
  width: 1.9rem;
  height: 1.9rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 0.68rem;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.45);
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}

/* ── Bubbles ── */
.chat-view__bubble {
  max-width: 70%;
  min-width: 0;
  border-radius: 1.35rem;
  padding: 0.72rem 1.05rem 0.5rem;
}

.chat-view__bubble--recv {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-bottom-left-radius: 0.3rem;
  backdrop-filter: blur(10px);
}

.chat-view__bubble--sent {
  background: linear-gradient(135deg, #7a023f, #3d0068);
  border: 1px solid rgba(192, 52, 94, 0.2);
  border-bottom-right-radius: 0.3rem;
  box-shadow: 0 5px 20px rgba(138, 3, 77, 0.32);
}

.chat-view__bubble p {
  margin: 0;
  font-size: 0.88rem;
  line-height: 1.5;
  color: rgba(240, 235, 255, 0.92);
  overflow-wrap: break-word;
  word-break: break-word;
}

.chat-view__bubble small {
  display: block;
  text-align: right;
  font-size: 0.64rem;
  color: rgba(195, 178, 228, 0.42);
  margin-top: 0.38rem;
}

/* ── Footer ── */
.chat-view__footer {
  padding: 0.85rem 1.1rem 1rem;
  border-top: 1px solid var(--cv-border);
  background: rgba(8, 1, 20, 0.6);
  backdrop-filter: blur(14px);
  flex-shrink: 0;
}

.chat-view__footer-body {
  max-width: 54rem;
  margin: 0 auto;
  width: 100%;
}

.chat-view__input-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 0;
  background: rgba(255, 255, 255, 0.035);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 1.5rem;
  padding: 0.3rem 0.3rem 0.3rem 0.55rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.chat-view__input-row:focus-within {
  border-color: rgba(90, 219, 148, 0.3);
  box-shadow: 0 0 0 3px rgba(90, 219, 148, 0.07), 0 4px 22px rgba(0, 0, 0, 0.3);
}

.chat-view__attach {
  background: none;
  border: none;
  color: var(--cv-muted);
  cursor: pointer;
  padding: 0.3rem 0.4rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 0.85rem;
  flex-shrink: 0;
  transition: color 0.15s, background 0.15s;
}

.chat-view__attach:hover {
  color: var(--cv-text);
  background: rgba(255, 255, 255, 0.07);
}

.chat-view__input {
  flex: 1;
  min-width: 0;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
  color: var(--cv-text) !important;
  padding: 0.52rem 0.4rem !important;
  font-size: 0.9rem !important;
}

.chat-view__input::placeholder { color: var(--cv-muted); }

.chat-view__send {
  width: 2.65rem !important;
  height: 2.65rem !important;
  padding: 0 !important;
  flex-shrink: 0;
  background: linear-gradient(135deg, #5adb94, #0ba18c) !important;
  border: none !important;
  color: #060010 !important;
  box-shadow: 0 4px 16px rgba(90, 219, 148, 0.3) !important;
  transition: filter 0.15s, transform 0.12s, box-shadow 0.15s !important;
}

.chat-view__send:not(:disabled):hover {
  filter: brightness(1.08) !important;
  transform: scale(1.06) !important;
  box-shadow: 0 7px 22px rgba(90, 219, 148, 0.44) !important;
}

.chat-view__send:disabled {
  opacity: 0.3 !important;
  box-shadow: none !important;
}
</style>
