<script setup lang="ts">
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import ChatView from '../components/chat/ChatView.vue'
import { useConversationStore } from '../stores/conversation'

const NARROW_QUERY = '(max-width: 980px)'

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

const store = useConversationStore()

const isNarrow = ref(false)
const mobileShowChat = ref(false)
const searchQuery = ref('')
const showNewConversationDialog = ref(false)

let mq: MediaQueryList | null = null

function refreshMq() {
  if (typeof window === 'undefined' || !mq) return
  isNarrow.value = mq.matches
  if (!mq.matches) mobileShowChat.value = false
}

onMounted(async () => {
  mq = window.matchMedia(NARROW_QUERY)
  refreshMq()
  mq.addEventListener('change', refreshMq)
  store.init()
  await store.loadConversations()
})

onUnmounted(() => {
  mq?.removeEventListener('change', refreshMq)
  store.cleanup()
})

watch(
  () => store.activeConversationId,
  (id) => {
    if (id !== null && isNarrow.value) mobileShowChat.value = true
  },
)

const activeConversation = computed(() => store.activeConversation)

const filteredConversations = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return store.conversations
  return store.conversations.filter((c) =>
    `${c.otherParticipant.name} ${c.lastMessage}`.toLowerCase().includes(q),
  )
})

function selectConv(id: number) {
  store.selectConversation(id)
}

function onChatBack() {
  if (isNarrow.value) {
    mobileShowChat.value = false
    return
  }
  store.clearActiveConversation()
}

async function confirmNewConversation() {
  await store.startConversation()
  showNewConversationDialog.value = false
}
</script>

<template>
  <div class="chat-page">
    <div class="chat-page__grid">
      <!-- Sidebar -->
      <aside
        class="chat-page__sidebar"
        :class="{ 'chat-page__sidebar--hidden': isNarrow && mobileShowChat }"
      >
        <div class="chat-page__sidebar-head">
          <div class="chat-page__title-row">
            <span class="chat-page__title-icon" aria-hidden="true">
              <i class="pi pi-comments"></i>
            </span>
            <h2 class="chat-page__sidebar-title">Conversas</h2>
          </div>
          <Button
            icon="pi pi-plus"
            rounded
            class="chat-page__add-btn"
            aria-label="Nova conversa"
            @click="showNewConversationDialog = true"
          />
        </div>

        <IconField class="chat-page__search-field">
          <InputIcon><i class="pi pi-search"></i></InputIcon>
          <InputText
            v-model="searchQuery"
            placeholder="Buscar conversas..."
            class="chat-page__search"
          />
        </IconField>

        <ul class="chat-page__list" role="list">
          <li v-for="c in filteredConversations" :key="c.id">
            <button
              type="button"
              class="chat-page__conv"
              :class="{ 'chat-page__conv--active': store.activeConversationId === c.id }"
              @click="selectConv(c.id)"
            >
              <div class="chat-page__av-wrap">
                <span
                  class="chat-page__mini-av"
                  :style="{ background: avatarGradient(c.otherParticipant.name) }"
                  aria-hidden="true"
                >{{ c.otherParticipant.name.charAt(0) }}</span>
                <span class="chat-page__online-dot" aria-hidden="true"></span>
              </div>

              <div class="chat-page__conv-body">
                <div class="chat-page__conv-row1">
                  <span class="chat-page__conv-name">{{ c.otherParticipant.name }}</span>
                  <span class="chat-page__conv-time">{{ c.activityLabel }}</span>
                </div>
                <p class="chat-page__conv-preview">{{ c.lastMessage }}</p>
                <div class="chat-page__conv-meta">
                  <span
                    v-if="c.score != null"
                    :class="['chat-page__score-pill', `chat-page__score-pill--${scoreLabel(c.score)}`]"
                  >
                    <i class="pi pi-chart-bar"></i> {{ c.score }}%
                  </span>
                  <span v-else class="chat-page__noscore">
                    <i class="pi pi-clock"></i> sem análise
                  </span>
                </div>
              </div>
            </button>
          </li>
        </ul>
      </aside>

      <!-- Content -->
      <section
        class="chat-page__content"
        :class="{ 'chat-page__content--hidden': isNarrow && !mobileShowChat }"
      >
        <ChatView
          v-if="activeConversation"
          :conversation="activeConversation"
          :messages="store.messages"
          :typing-visible="store.typingVisible"
          @back="onChatBack"
        />
        <div v-else class="chat-page__empty">
          <div class="chat-page__empty-icon-wrap">
            <i class="pi pi-comments chat-page__empty-icon" aria-hidden="true"></i>
          </div>
          <p class="chat-page__empty-title">Nenhuma conversa selecionada</p>
          <p class="chat-page__empty-sub">Escolha uma conversa na lista ao lado para começar.</p>
        </div>
      </section>
    </div>

    <!-- Dialog nova conversa -->
    <Dialog
      v-model:visible="showNewConversationDialog"
      modal
      header="Nova conversa"
      class="new-conv-dialog"
      :style="{ width: '22rem' }"
    >
      <p class="new-conv-dialog__text">
        Deseja iniciar uma nova conversa com uma pessoa aleatória?
      </p>
      <template #footer>
        <Button
          label="Cancelar"
          text
          class="new-conv-dialog__cancel"
          @click="showNewConversationDialog = false"
        />
        <Button
          label="Confirmar"
          class="new-conv-dialog__confirm"
          :loading="store.creatingConversation"
          @click="confirmNewConversation"
        />
      </template>
    </Dialog>
  </div>
</template>

<style scoped>
/* ── Design tokens ── */
.chat-page {
  --bg: #0c0017;
  --surface: rgba(18, 4, 32, 0.93);
  --surface-hover: rgba(26, 8, 46, 0.92);
  --surface-active: rgba(36, 12, 62, 0.9);
  --border: rgba(90, 219, 148, 0.11);
  --accent: #5adb94;
  --accent-glow: rgba(90, 219, 148, 0.2);
  --muted: rgba(195, 178, 228, 0.5);
  --text: #f0ebff;

  width: 100%;
  min-width: 0;
  height: 100vh;
  max-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 1rem 1.25rem 1.25rem;
  box-sizing: border-box;
  overflow: hidden;

  /* Mesh gradient background */
  background-color: var(--bg);
  background-image:
    radial-gradient(ellipse 60% 50% at 8% 0%,   rgba(138, 3, 77, 0.22)  0%, transparent 65%),
    radial-gradient(ellipse 45% 40% at 92% 100%, rgba(90, 219, 148, 0.12) 0%, transparent 65%),
    radial-gradient(ellipse 50% 45% at 50% 50%,  rgba(55, 0, 100, 0.3)   0%, transparent 75%);
}

@supports (height: 100dvh) {
  .chat-page { height: 100dvh; max-height: 100dvh; }
}

/* ── Grid ── */
.chat-page__grid {
  flex: 1 1 auto;
  min-height: 0;
  display: grid;
  grid-template-columns: minmax(16rem, 26%) 1fr;
  grid-template-rows: minmax(0, 1fr);
  gap: 1rem;
  align-items: stretch;
}

/* ── Sidebar ── */
.chat-page__sidebar {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  min-height: 0;
  height: 100%;
  max-height: 100%;
  padding: 1.1rem 0.9rem;
  background: var(--surface);
  backdrop-filter: blur(28px) saturate(160%);
  border: 1px solid var(--border);
  border-radius: 1.5rem;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.04),
    0 24px 64px rgba(0, 0, 0, 0.65),
    0 0 48px rgba(138, 3, 77, 0.07);
}

.chat-page__sidebar-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0 0.2rem;
}

.chat-page__title-row {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}

.chat-page__title-icon {
  display: grid;
  place-items: center;
  width: 2rem;
  height: 2rem;
  border-radius: 0.65rem;
  background: linear-gradient(135deg, rgba(90, 219, 148, 0.18), rgba(11, 161, 140, 0.1));
  border: 1px solid rgba(90, 219, 148, 0.22);
  color: var(--accent);
  font-size: 0.8rem;
  box-shadow: 0 0 14px rgba(90, 219, 148, 0.1);
}

.chat-page__sidebar-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.025em;
}

.chat-page__add-btn {
  width: 2.2rem !important;
  height: 2.2rem !important;
  padding: 0 !important;
  flex-shrink: 0;
  border-radius: 50% !important;
  background: linear-gradient(135deg, rgba(90, 219, 148, 0.18), rgba(11, 161, 140, 0.1)) !important;
  border: 1px solid rgba(90, 219, 148, 0.3) !important;
  color: var(--accent) !important;
  box-shadow: 0 0 14px rgba(90, 219, 148, 0.12) !important;
  transition: transform 0.18s ease, box-shadow 0.18s ease !important;
}

.chat-page__add-btn:hover {
  transform: scale(1.08) rotate(90deg) !important;
  box-shadow: 0 0 24px rgba(90, 219, 148, 0.28) !important;
}

/* ── Search ── */
.chat-page__search-field { width: 100%; }

.chat-page__search-field :deep(.p-inputicon) {
  color: var(--muted);
  font-size: 0.78rem;
}

.chat-page__search {
  width: 100%;
  border-radius: 999px !important;
  background: rgba(255, 255, 255, 0.035) !important;
  border: 1px solid rgba(255, 255, 255, 0.07) !important;
  color: var(--text) !important;
  padding-left: 2.4rem !important;
  font-size: 0.84rem !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}

.chat-page__search:focus {
  border-color: rgba(90, 219, 148, 0.35) !important;
  box-shadow: 0 0 0 3px rgba(90, 219, 148, 0.08) !important;
}

.chat-page__search::placeholder { color: var(--muted); }

/* ── Conversation list ── */
.chat-page__list {
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  scrollbar-width: thin;
  scrollbar-color: rgba(90, 219, 148, 0.12) transparent;
}

/* ── Conv item ── */
.chat-page__conv {
  width: 100%;
  display: flex;
  align-items: flex-start;
  gap: 0.7rem;
  padding: 0.7rem 0.55rem;
  border: none;
  border-left: 2.5px solid transparent;
  border-radius: 0.95rem;
  background: transparent;
  cursor: pointer;
  text-align: left;
  font: inherit;
  color: inherit;
  transition: background 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}

.chat-page__conv:hover {
  background: var(--surface-hover);
}

.chat-page__conv--active {
  background: var(--surface-active) !important;
  border-left-color: var(--accent);
  box-shadow:
    inset 0 0 30px rgba(90, 219, 148, 0.04),
    0 2px 14px rgba(0, 0, 0, 0.35);
}

/* Avatar */
.chat-page__av-wrap {
  position: relative;
  flex-shrink: 0;
}

.chat-page__mini-av {
  width: 2.65rem;
  height: 2.65rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 0.88rem;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.45);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
}

.chat-page__online-dot {
  position: absolute;
  bottom: 1px;
  right: 1px;
  width: 0.6rem;
  height: 0.6rem;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid rgba(12, 0, 23, 0.95);
  box-shadow: 0 0 7px rgba(90, 219, 148, 0.6);
}

/* Conv body */
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
  gap: 0.4rem;
}

.chat-page__conv-name {
  font-size: 0.87rem;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-page__conv-time {
  font-size: 0.67rem;
  color: var(--muted);
  flex-shrink: 0;
}

.chat-page__conv-preview {
  margin: 0;
  font-size: 0.75rem;
  color: var(--muted);
  line-height: 1.35;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-page__conv-meta {
  margin-top: 0.1rem;
  display: flex;
  align-items: center;
}

/* Score pill */
.chat-page__score-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.22rem;
  padding: 0.12rem 0.5rem;
  border-radius: 999px;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.chat-page__score-pill .pi { font-size: 0.58rem; }

.chat-page__score-pill--high {
  background: rgba(90, 219, 148, 0.12);
  color: #5adb94;
  border: 1px solid rgba(90, 219, 148, 0.25);
}

.chat-page__score-pill--mid {
  background: rgba(251, 191, 36, 0.11);
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.22);
}

.chat-page__score-pill--low {
  background: rgba(248, 113, 113, 0.11);
  color: #f87171;
  border: 1px solid rgba(248, 113, 113, 0.22);
}

.chat-page__noscore {
  display: inline-flex;
  align-items: center;
  gap: 0.22rem;
  font-size: 0.65rem;
  color: var(--muted);
}

.chat-page__noscore .pi { font-size: 0.58rem; }

/* ── Content ── */
.chat-page__content {
  min-width: 0;
  min-height: 0;
  height: 100%;
  max-height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-page__content > :deep(.chat-view) {
  flex: 1;
  min-height: 0;
}

/* ── Empty state ── */
.chat-page__empty {
  flex: 1;
  min-height: 12rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  text-align: center;
  background: var(--surface);
  backdrop-filter: blur(28px);
  border: 1px solid var(--border);
  border-radius: 1.5rem;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.55);
}

.chat-page__empty-icon-wrap {
  width: 4.5rem;
  height: 4.5rem;
  display: grid;
  place-items: center;
  border-radius: 1.35rem;
  background: linear-gradient(135deg, rgba(90, 219, 148, 0.12), rgba(11, 161, 140, 0.06));
  border: 1px solid rgba(90, 219, 148, 0.18);
  box-shadow: 0 0 28px rgba(90, 219, 148, 0.1);
}

.chat-page__empty-icon {
  font-size: 1.7rem;
  color: var(--accent);
  opacity: 0.85;
}

.chat-page__empty-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: rgba(240, 235, 255, 0.7);
}

.chat-page__empty-sub {
  margin: 0;
  font-size: 0.78rem;
  color: var(--muted);
  max-width: 18rem;
  line-height: 1.55;
}

/* ── Dialog ── */
:deep(.new-conv-dialog) {
  background: rgba(16, 4, 28, 0.97);
  border: 1px solid rgba(90, 219, 148, 0.18);
  border-radius: 1.35rem;
  backdrop-filter: blur(28px);
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.75), 0 0 40px rgba(138, 3, 77, 0.12);
}

:deep(.new-conv-dialog .p-dialog-header) {
  background: transparent;
  color: #f0ebff;
  border-bottom: 1px solid rgba(90, 219, 148, 0.1);
  border-radius: 1.35rem 1.35rem 0 0;
  padding: 1.1rem 1.5rem;
}

:deep(.new-conv-dialog .p-dialog-title) {
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

:deep(.new-conv-dialog .p-dialog-content) {
  background: transparent;
  padding: 1.25rem 1.5rem;
}

:deep(.new-conv-dialog .p-dialog-footer) {
  background: transparent;
  border-top: 1px solid rgba(90, 219, 148, 0.08);
  border-radius: 0 0 1.35rem 1.35rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 0.85rem 1.5rem;
}

.new-conv-dialog__text {
  margin: 0;
  color: rgba(240, 235, 255, 0.75);
  font-size: 0.9rem;
  line-height: 1.55;
}

:deep(.new-conv-dialog__cancel) {
  color: rgba(195, 178, 228, 0.65) !important;
}

:deep(.new-conv-dialog__cancel:hover) {
  color: #f0ebff !important;
  background: rgba(255, 255, 255, 0.06) !important;
}

:deep(.new-conv-dialog__confirm) {
  background: linear-gradient(135deg, rgba(90, 219, 148, 0.18), rgba(11, 161, 140, 0.1)) !important;
  border: 1px solid rgba(90, 219, 148, 0.35) !important;
  color: #5adb94 !important;
  font-weight: 700 !important;
  transition: box-shadow 0.18s !important;
}

:deep(.new-conv-dialog__confirm:hover) {
  background: linear-gradient(135deg, rgba(90, 219, 148, 0.28), rgba(11, 161, 140, 0.18)) !important;
  box-shadow: 0 0 18px rgba(90, 219, 148, 0.18) !important;
}

/* ── Mobile ── */
@media (max-width: 980px) {
  .chat-page {
    padding: 0.65rem 0.65rem 0.75rem;
  }

  .chat-page__grid {
    grid-template-columns: 1fr;
    grid-template-rows: minmax(0, 1fr);
  }

  .chat-page__sidebar--hidden,
  .chat-page__content--hidden {
    display: none;
  }
}
</style>
