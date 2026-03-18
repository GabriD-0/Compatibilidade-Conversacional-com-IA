<script setup lang="ts">
import Button from 'primevue/button'
import Listbox from 'primevue/listbox'
import Tag from 'primevue/tag'
import { computed, ref } from 'vue'
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
  messages: Message[]
}

const conversations = ref<Conversation[]>([
  {
    id: '1',
    participantA: 'Ana',
    participantB: 'Bruno',
    avatarColorA: 'bg-primary',
    avatarColorB: 'bg-secondary',
    score: 87,
    messages: [
      { id: '1-1', sender: 'A', text: 'Gostei da proposta para o TCC.', time: '14:30' },
      { id: '1-2', sender: 'B', text: 'Tambem curti, achei bem alinhada.', time: '14:31' },
    ],
  },
  {
    id: '2',
    participantA: 'Carla',
    participantB: 'Diego',
    avatarColorA: 'bg-accent',
    avatarColorB: 'bg-secondary',
    score: 72,
    messages: [
      { id: '2-1', sender: 'A', text: 'Vamos revisar os requisitos?', time: '15:10' },
      { id: '2-2', sender: 'B', text: 'Fechado, começo pelos fluxos.', time: '15:11' },
    ],
  },
])

const activeId = ref<string>('1')

const activeConversation = computed(
  () => conversations.value.find((conversation) => conversation.id === activeId.value) ?? null,
)

const listItems = computed(() =>
  conversations.value.map((conversation) => ({
    label: `${conversation.participantA} & ${conversation.participantB}`,
    value: conversation.id,
    score: conversation.score,
  })),
)
</script>

<template>
  <div class="chat-page">
    <aside class="chat-page__sidebar card">
      <h2>Conversas</h2>
      <Listbox v-model="activeId" :options="listItems" option-label="label" option-value="value">
        <template #option="slotProps">
          <div class="chat-page__item">
            <span>{{ slotProps.option.label }}</span>
            <Tag :value="`Score ${slotProps.option.score ?? '-'}`" severity="success" />
          </div>
        </template>
      </Listbox>
      <Button label="Nova conversa" icon="pi pi-plus" size="small" />
    </aside>

    <section class="chat-page__content">
      <ChatView
        v-if="activeConversation"
        :conversation="activeConversation"
        @back="activeId = conversations[0]?.id ?? ''"
      />
      <div v-else class="chat-page__empty card">
        <p>Selecione uma conversa para comecar.</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.chat-page {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 1rem;
  height: calc(100vh - 8.4rem);
}

.chat-page__sidebar {
  display: grid;
  gap: 0.75rem;
  align-content: start;
}

.chat-page__item {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.chat-page__content {
  min-width: 0;
}

.chat-page__empty {
  height: 100%;
  display: grid;
  place-items: center;
}

@media (max-width: 980px) {
  .chat-page {
    grid-template-columns: 1fr;
    height: auto;
  }
}
</style>
