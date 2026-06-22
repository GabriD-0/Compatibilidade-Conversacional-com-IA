import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import { conversationsApi, extractApiError, extractApiErrorCode } from '../services/api'
import { connectSocket, disconnectSocket, joinConversation, leaveConversation, sendMessage as socketSendMessage, emitTyping, emitRead, onNewMessage, onUserTyping, onMessageStatus, onAnalysisUpdated } from '../services/socket'
import type { Conversation, ConversationAnalysis, AnalysisClassification, WsNewMessage, WsUserTyping, WsMessageStatus, WsAnalysisUpdated, MessageStatus } from '../types/types'

export interface UiConversation {
  id: number
  otherParticipant: { id: number; name: string }
  lastMessage: string
  lastMessageAt: string | null
  messageCount: number
  score: number | null
  classification: AnalysisClassification | null
  lastAnalysisAt: string | null
  activityLabel: string
}

export interface UiMessage {
  id: number | string
  senderId: number
  content: string
  sentAt: string
  position: number
  status: MessageStatus
  optimistic?: true
}

function formatRelative(iso: string | null): string {
  if (!iso) return ''
  const diff = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diff / 60_000)
  if (mins < 1) return 'Agora'
  if (mins < 60) return `${mins} min`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs} h`
  return `${Math.floor(hrs / 24)} d`
}

export const useConversationStore = defineStore('conversation', () => {
  const authStore = useAuthStore()
  const conversations = ref<UiConversation[]>([])
  const activeConversationId = ref<number | null>(null)
  const messages = ref<UiMessage[]>([])
  const loadingConversations = ref(false)
  const loadingMessages = ref(false)
  const loadingAnalysis = ref(false)
  const creatingConversation = ref(false)
  const typingVisible = ref(false)
  const error = ref<string | null>(null)
  const activeAnalysis = ref<ConversationAnalysis | null>(null)
  const analysisError = ref<string | null>(null)

  let typingTimer: ReturnType<typeof setTimeout> | null = null
  let socketCleanups: Array<() => void> = []
  let analysisRequestSeq = 0

  const myId = computed(() => authStore.user?.id ?? 0)

  const activeConversation = computed<UiConversation | null>(
    () => conversations.value.find((conversation) => conversation.id === activeConversationId.value) ?? null,
  )

  function buildUiConversation(raw: Conversation): UiConversation {
    const other =
      raw.participant_a.id === myId.value
        ? (raw.participant_b ?? raw.participant_a)
        : raw.participant_a
    return {
      id: raw.id,
      otherParticipant: other,
      lastMessage: '',
      lastMessageAt: raw.last_message_at,
      messageCount: raw.message_count,
      score: raw.score,
      classification: raw.classification,
      lastAnalysisAt: raw.last_analysis_at,
      activityLabel: formatRelative(raw.last_message_at),
    }
  }

  function init() {
    connectSocket()
    socketCleanups.push(onNewMessage(handleNewMessage))
    socketCleanups.push(onUserTyping(handleUserTyping))
    socketCleanups.push(onMessageStatus(handleMessageStatusEvent))
    socketCleanups.push(onAnalysisUpdated(handleAnalysisUpdated))
  }

  function cleanup() {
    socketCleanups.forEach((fn) => fn())
    socketCleanups = []
    if (activeConversationId.value !== null) {
      leaveConversation(activeConversationId.value)
    }
    disconnectSocket()
  }

  async function loadConversations() {
    loadingConversations.value = true
    error.value = null
    try {
      const page = await conversationsApi.list()
      conversations.value = page.conversations.map((conversation) => buildUiConversation(conversation))
    } catch (err) {
      error.value = extractApiError(err)
    } finally {
      loadingConversations.value = false
    }
  }

  async function selectConversation(id: number) {
    if (activeConversationId.value !== null && activeConversationId.value !== id) {
      leaveConversation(activeConversationId.value)
    }

    activeConversationId.value = id
    messages.value = []
    activeAnalysis.value = null
    analysisError.value = null

    await Promise.all([loadMessages(id), loadActiveAnalysis(id)])
    if (activeConversationId.value !== id) return

    try {
      await joinConversation(id)
    } catch {
      // sala pode não existir ainda se conversa foi criada agora
      console.error('Sala não existe ainda se conversa foi criada agora')
    }
  }

  async function loadActiveAnalysis(id: number) {
    const requestSeq = ++analysisRequestSeq
    loadingAnalysis.value = true
    analysisError.value = null

    try {
      const analysis = await conversationsApi.getAnalysis(id)
      if (activeConversationId.value === id && requestSeq === analysisRequestSeq) {
        applyAnalysis(analysis)
      }
    } catch (err) {
      if (activeConversationId.value !== id || requestSeq !== analysisRequestSeq) return
      if (extractApiErrorCode(err) === 'analysis_not_found') {
        activeAnalysis.value = null
        return
      }
      analysisError.value = extractApiError(err)
    } finally {
      if (activeConversationId.value === id && requestSeq === analysisRequestSeq) {
        loadingAnalysis.value = false
      }
    }
  }

  async function loadMessages(id: number) {
    loadingMessages.value = true
    try {
      const page = await conversationsApi.messages(id)
      if (activeConversationId.value === id) {
        messages.value = page.messages.map((message) => ({
          id: message.id,
          senderId: message.sender_id,
          content: message.content,
          sentAt: message.sent_at,
          position: message.position,
          status: message.status,
        }))
      }
    } catch (err) {
      if (activeConversationId.value === id) {
        error.value = extractApiError(err)
      }
    } finally {
      if (activeConversationId.value === id) {
        loadingMessages.value = false
      }
    }
  }

  async function sendMessage(content: string) {
    const trimmed = content.trim()
    if (!trimmed || trimmed.length > 4096 || activeConversationId.value === null) return

    const tempId = `temp-${Date.now()}`
    const optimistic: UiMessage = {
      id: tempId,
      senderId: myId.value,
      content: trimmed,
      sentAt: new Date().toISOString(),
      position: -1,
      status: 'sent',
      optimistic: true,
    }
    messages.value.push(optimistic)

    try {
      await socketSendMessage(activeConversationId.value, trimmed)
    } catch {
      messages.value = messages.value.filter((message) => message.id !== tempId)
      error.value = 'Falha ao enviar mensagem. Tente novamente.'
    }
  }

  async function analyzeActiveConversation() {
    if (activeConversationId.value === null || loadingAnalysis.value) return

    const conversationId = activeConversationId.value
    const requestSeq = ++analysisRequestSeq
    loadingAnalysis.value = true
    analysisError.value = null

    try {
      const analysis = await conversationsApi.analyze(conversationId)
      if (activeConversationId.value === conversationId && requestSeq === analysisRequestSeq) {
        applyAnalysis(analysis)
      }
    } catch (err) {
      if (activeConversationId.value === conversationId && requestSeq === analysisRequestSeq) {
        analysisError.value = extractApiError(err)
      }
    } finally {
      if (activeConversationId.value === conversationId && requestSeq === analysisRequestSeq) {
        loadingAnalysis.value = false
      }
    }
  }

  async function startConversation(participantId?: number) {
    creatingConversation.value = true
    error.value = null
    try {
      const conv = await conversationsApi.create(participantId)
      const uiConv = buildUiConversation(conv)
      const existing = conversations.value.findIndex((conversation) => conversation.id === conv.id)
      if (existing === -1) conversations.value.unshift(uiConv)
      await selectConversation(conv.id)
    } catch (err) {
      error.value = extractApiError(err)
      throw err
    } finally {
      creatingConversation.value = false
    }
  }

  async function removeConversation(id: number) {
    try {
      await conversationsApi.delete(id)
      conversations.value = conversations.value.filter((conversation) => conversation.id !== id)
      if (activeConversationId.value === id) {
        analysisRequestSeq++
        activeConversationId.value = null
        messages.value = []
        activeAnalysis.value = null
        loadingMessages.value = false
        loadingAnalysis.value = false
        analysisError.value = null
      }
    } catch (err) {
      error.value = extractApiError(err)
    }
  }

  function applyAnalysis(analysis: ConversationAnalysis) {
    const conversation = conversations.value.find((item) => item.id === analysis.conversation_id)
    if (conversation) {
      conversation.score = Math.round(analysis.score)
      conversation.classification = analysis.classification
      conversation.lastAnalysisAt = analysis.computed_at
    }

    if (activeConversationId.value === analysis.conversation_id) {
      activeAnalysis.value = analysis
      analysisError.value = null
    }
  }

  function handleNewMessage(data: WsNewMessage) {
    if (data.sender_id === myId.value) {
      // Remove mensagem otimista com mesmo conteúdo
      const optIdx = messages.value.findIndex(
        (message) => message.optimistic && message.content === data.content && message.senderId === data.sender_id,
      )
      if (optIdx !== -1) messages.value.splice(optIdx, 1)
    }

    // Evita duplicata
    if (messages.value.some((message) => message.id === data.id)) return

    messages.value.push({
      id: data.id,
      senderId: data.sender_id,
      content: data.content,
      sentAt: data.sent_at,
      position: data.position,
      status: data.status,
    })

    // Atualiza sidebar
    const conv = conversations.value.find((conversation) => conversation.id === activeConversationId.value)
    if (conv) {
      conv.lastMessage = data.content
      conv.lastMessageAt = data.sent_at
      conv.messageCount++
      conv.activityLabel = formatRelative(data.sent_at)
    }

    // Auto-read de mensagens recebidas enquanto a conversa está aberta
    if (data.sender_id !== myId.value && activeConversationId.value !== null) {
      emitRead(activeConversationId.value, data.position)
    }
  }

  function handleUserTyping(data: WsUserTyping) {
    if (data.sender_id === myId.value) return
    typingVisible.value = true
    if (typingTimer) clearTimeout(typingTimer)
    typingTimer = setTimeout(() => {
      typingVisible.value = false
    }, 3000)
  }

  function handleMessageStatusEvent(data: WsMessageStatus) {
    messages.value.forEach((message) => {
      if (
        typeof message.position === 'number' &&
        message.position <= data.up_to_position &&
        message.status !== 'read'
      ) {
        message.status = data.status
      }
    })
  }

  function handleAnalysisUpdated(data: WsAnalysisUpdated) {
    applyAnalysis(data)
  }

  function clearActiveConversation() {
    analysisRequestSeq++
    activeConversationId.value = null
    messages.value = []
    activeAnalysis.value = null
    loadingMessages.value = false
    loadingAnalysis.value = false
    analysisError.value = null
  }

  // Expõe emitTyping para uso no ChatView
  function emitTypingForActiveConversation() {
    if (activeConversationId.value !== null) {
      emitTyping(activeConversationId.value)
    }
  }

  return {
    conversations,
    activeConversationId,
    messages,
    loadingConversations,
    loadingMessages,
    loadingAnalysis,
    creatingConversation,
    typingVisible,
    error,
    activeAnalysis,
    analysisError,
    activeConversation,
    myId,
    init,
    cleanup,
    loadConversations,
    selectConversation,
    sendMessage,
    analyzeActiveConversation,
    startConversation,
    removeConversation,
    clearActiveConversation,
    emitTypingForActiveConversation,
  }
})
