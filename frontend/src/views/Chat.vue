<script setup lang="ts">
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import ChatView from '../components/chat/ChatView.vue'

type Sender = 'A' | 'B'
type Message = { id: string; sender: Sender; text: string; time: string }
type Conversation = {
  id: string
  participantA: string
  participantB: string
  avatarColorA: string
  avatarColorB: string
  score: number | null
  activityLabel: string
  messages: Message[]
}

const NARROW_QUERY = '(max-width: 980px)'

const conversations = ref<Conversation[]>([
  {
    id: '1',
    participantA: 'Ana',
    participantB: 'Bruno',
    avatarColorA: 'bg-primary',
    avatarColorB: 'bg-secondary',
    score: 87,
    activityLabel: 'Agora',
    messages: [
      { id: '1-1', sender: 'A', text: 'Gostei da proposta para o TCC.', time: '14:28' },
      { id: '1-2', sender: 'B', text: 'Também curti, achei bem alinhada.', time: '14:29' },
      { id: '1-3', sender: 'A', text: 'Você acha que dá para entregar na semana 12?', time: '14:30' },
      { id: '1-4', sender: 'B', text: 'Sim, se mantivermos o escopo atual.', time: '14:31' },
      { id: '1-5', sender: 'A', text: 'Perfeito, monto o cronograma hoje.', time: '14:32' },
      { id: '1-6', sender: 'B', text: 'Combinado. Te aviso se surgir bloqueio.', time: '14:33' },
    ],
  },
  {
    id: '2',
    participantA: 'Carla',
    participantB: 'Diego',
    avatarColorA: 'bg-accent',
    avatarColorB: 'bg-secondary',
    score: 72,
    activityLabel: '5 min',
    messages: [
      { id: '2-1', sender: 'A', text: 'Vamos revisar os requisitos?', time: '15:10' },
      { id: '2-2', sender: 'B', text: 'Fechado, começo pelos fluxos.', time: '15:11' },
    ],
  },
  {
    id: '3',
    participantA: 'Elena',
    participantB: 'Felipe',
    avatarColorA: 'bg-primary',
    avatarColorB: 'bg-accent',
    score: null,
    activityLabel: '1 h',
    messages: [{ id: '3-1', sender: 'A', text: 'Te mando o arquivo amanhã.', time: '09:00' }],
  },
])

const activeId = ref<string | null>('1')
const isNarrow = ref(false)
const mobileShowChat = ref(false)
const searchQuery = ref('')

let mq: MediaQueryList | null = null

function refreshMq() {
  if (typeof window === 'undefined' || !mq) return
  isNarrow.value = mq.matches
  if (!mq.matches) {
    mobileShowChat.value = false
  }
}

onMounted(() => {
  mq = window.matchMedia(NARROW_QUERY)
  refreshMq()
  mq.addEventListener('change', refreshMq)
})

onUnmounted(() => {
  mq?.removeEventListener('change', refreshMq)
})

watch(activeId, (id) => {
  if (id && isNarrow.value) {
    mobileShowChat.value = true
  }
})

const activeConversation = computed(
  () => conversations.value.find((conversation) => conversation.id === activeId.value) ?? null,
)

function lastPreview(c: Conversation): string {
  const last = c.messages[c.messages.length - 1]
  return last?.text ?? ''
}

const filteredConversations = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return conversations.value
  return conversations.value.filter((c) => {
    const hay = `${c.participantA} ${c.participantB} ${lastPreview(c)}`.toLowerCase()
    return hay.includes(q)
  })
})

function onChatBack() {
  if (isNarrow.value) {
    mobileShowChat.value = false
    return
  }
  activeId.value = null
}
</script>

<template>
  <div class="chat-page">
    <div class="chat-page__grid">
      <aside
        class="chat-page__sidebar"
        :class="{ 'chat-page__sidebar--hidden': isNarrow && mobileShowChat }"
      >
        <div class="chat-page__sidebar-head">
          <h2 class="chat-page__sidebar-title">Conversas</h2>
          <Button
            icon="pi pi-plus"
            rounded
            class="chat-page__add-btn"
            aria-label="Nova conversa"
          />
        </div>

        <IconField class="chat-page__search-field">
          <InputIcon>
            <i class="pi pi-search"></i>
          </InputIcon>
          <InputText v-model="searchQuery" placeholder="Buscar conversas..." class="chat-page__search" />
        </IconField>

        <ul class="chat-page__list" role="list">
          <li v-for="c in filteredConversations" :key="c.id">
            <button
              type="button"
              class="chat-page__conv"
              :class="{ 'chat-page__conv--active': activeId === c.id }"
              @click="activeId = c.id"
            >
              <div class="chat-page__stack" aria-hidden="true">
                <span :class="['chat-page__mini-av', c.avatarColorA]">{{ c.participantA.charAt(0) }}</span>
                <span :class="['chat-page__mini-av', c.avatarColorB]">{{ c.participantB.charAt(0) }}</span>
              </div>
              <div class="chat-page__conv-body">
                <div class="chat-page__conv-row1">
                  <span class="chat-page__conv-name">{{ c.participantA }} &amp; {{ c.participantB }}</span>
                  <span class="chat-page__conv-time">{{ c.activityLabel }}</span>
                </div>
                <p class="chat-page__conv-preview">{{ lastPreview(c) }}</p>
                <p v-if="c.score != null" class="chat-page__conv-score">score: {{ c.score }}</p>
                <p v-else class="chat-page__conv-noscore">sem análise</p>
              </div>
            </button>
          </li>
        </ul>
      </aside>

      <section
        class="chat-page__content"
        :class="{ 'chat-page__content--hidden': isNarrow && !mobileShowChat }"
      >
        <ChatView v-if="activeConversation" :conversation="activeConversation" @back="onChatBack" />
        <div v-else class="chat-page__empty">
          <i class="pi pi-comments chat-page__empty-icon" aria-hidden="true"></i>
          <p>Selecione uma conversa para começar.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.chat-page {
  --chat-deep: #1a0d24;
  --chat-panel: #231530;
  --chat-panel-hover: #2d1c42;
  --chat-row-active: #352048;
  --chat-border: rgba(90, 219, 148, 0.22);
  --chat-accent: #5adb94;
  --chat-muted: rgba(255, 255, 255, 0.55);
  --chat-input-bg: #150a1c;

  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  padding: 1rem 1.25rem 1.25rem;
  box-sizing: border-box;
  background: var(--chat-deep);
}

.chat-page__grid {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: minmax(17rem, 28%) 1fr;
  gap: 1rem;
  align-items: stretch;
}

.chat-page__sidebar {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  min-height: 0;
  padding: 1rem 0.85rem;
  background: var(--chat-panel);
  border: 1px solid var(--chat-border);
  border-radius: 1.25rem;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
}

.chat-page__sidebar-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0 0.15rem;
}

.chat-page__sidebar-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.02em;
}

.chat-page__add-btn {
  width: 2.25rem !important;
  height: 2.25rem !important;
  padding: 0 !important;
  flex-shrink: 0;
  border-radius: 50% !important;
  background: rgba(90, 219, 148, 0.12) !important;
  border: 1px solid rgba(90, 219, 148, 0.35) !important;
  color: var(--chat-accent) !important;
}

.chat-page__add-btn:hover {
  background: rgba(90, 219, 148, 0.22) !important;
}

.chat-page__search-field {
  width: 100%;
}

.chat-page__search-field :deep(.p-inputicon) {
  color: var(--chat-muted);
}

.chat-page__search {
  width: 100%;
  border-radius: 999px !important;
  background: var(--chat-input-bg) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  color: #fff !important;
  padding-left: 2.35rem !important;
  font-size: 0.9rem !important;
}

.chat-page__search::placeholder {
  color: var(--chat-muted);
}

.chat-page__list {
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.chat-page__conv {
  width: 100%;
  display: flex;
  align-items: flex-start;
  gap: 0.65rem;
  padding: 0.65rem 0.5rem;
  border: none;
  border-radius: 0.85rem;
  background: transparent;
  cursor: pointer;
  text-align: left;
  font: inherit;
  color: inherit;
  transition: background-color 0.15s ease;
}

.chat-page__conv:hover {
  background: var(--chat-panel-hover);
}

.chat-page__conv--active {
  background: var(--chat-row-active);
}

.chat-page__stack {
  position: relative;
  width: 2.6rem;
  height: 2rem;
  flex-shrink: 0;
}

.chat-page__mini-av {
  position: absolute;
  width: 1.55rem;
  height: 1.55rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 0.62rem;
  font-weight: 700;
  color: #fff;
  border: 2px solid var(--chat-panel);
  box-sizing: border-box;
}

.chat-page__mini-av:first-child {
  left: 0;
  top: 0;
  z-index: 1;
}

.chat-page__mini-av:last-child {
  left: 0.85rem;
  top: 0.15rem;
  z-index: 2;
}

.chat-page__conv--active .chat-page__mini-av {
  border-color: var(--chat-row-active);
}

.chat-page__conv-body {
  min-width: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.chat-page__conv-row1 {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 0.5rem;
}

.chat-page__conv-name {
  font-size: 0.88rem;
  font-weight: 600;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-page__conv-time {
  font-size: 0.72rem;
  color: var(--chat-muted);
  flex-shrink: 0;
}

.chat-page__conv-preview {
  margin: 0;
  font-size: 0.78rem;
  color: var(--chat-muted);
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.chat-page__conv-score {
  margin: 0.1rem 0 0;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--chat-accent);
}

.chat-page__conv-noscore {
  margin: 0.1rem 0 0;
  font-size: 0.72rem;
  color: var(--chat-muted);
}

.chat-page__content {
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.chat-page__content > :deep(.chat-view) {
  flex: 1;
  min-height: 0;
}

.chat-page__empty {
  flex: 1;
  min-height: 12rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  text-align: center;
  color: var(--chat-muted);
  background: var(--chat-panel);
  border: 1px solid var(--chat-border);
  border-radius: 1.25rem;
}

.chat-page__empty p {
  margin: 0;
}

.chat-page__empty-icon {
  font-size: 2rem;
  opacity: 0.45;
  color: var(--chat-accent);
}

@media (max-width: 980px) {
  .chat-page__grid {
    grid-template-columns: 1fr;
  }

  .chat-page__sidebar--hidden,
  .chat-page__content--hidden {
    display: none;
  }

  .chat-page__sidebar:not(.chat-page__sidebar--hidden) {
    min-height: min(52vh, 30rem);
  }

  .chat-page__content:not(.chat-page__content--hidden) {
    min-height: min(72vh, 38rem);
  }
}

@media (prefers-color-scheme: light) {
  .chat-page {
    --chat-deep: #f1f0f5;
    --chat-panel: #ffffff;
    --chat-panel-hover: #ede9f4;
    --chat-row-active: #e8e0f2;
    --chat-border: rgba(11, 161, 140, 0.2);
    --chat-muted: rgba(33, 53, 71, 0.62);
    --chat-input-bg: #f6f4fa;
  }

  .chat-page__sidebar-title,
  .chat-page__conv-name {
    color: #1e1530;
  }

  .chat-page__search {
    color: #1e1530 !important;
  }

  .chat-page__mini-av {
    border-color: var(--chat-panel);
  }

  .chat-page__conv--active .chat-page__mini-av {
    border-color: var(--chat-row-active);
  }

  .chat-page__empty {
    color: var(--chat-muted);
  }
}
</style>
