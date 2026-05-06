export interface ApiErrorPayload {
  code: string
  message: string
}

export interface ApiErrorResponse {
  error: ApiErrorPayload
}

export interface AuthUser {
  id: number
  email: string
  name: string
}

export interface AuthResponse {
  user: AuthUser
  access_token: string
  refresh_token: string
}

export interface RefreshResponse {
  access_token: string
}

// ---- Conversation domain ----

export interface ConversationParticipant {
  id: number
  name: string
}

export interface Conversation {
  id: number
  participant_a: ConversationParticipant
  participant_b: ConversationParticipant | null
  message_count: number
  last_message_at: string | null
  created_at: string
}

export interface ConversationsPage {
  conversations: Conversation[]
  total: number
  page: number
  per_page: number
}

export type MessageStatus = 'sent' | 'read'

export interface Message {
  id: number
  sender_id: number
  content: string
  sent_at: string
  position: number
  status: MessageStatus
}

export interface MessagesPage {
  messages: Message[]
}

// ---- WebSocket broadcast payloads ----

export interface WsNewMessage {
  id: number
  sender_id: number
  content: string
  sent_at: string
  position: number
  status: MessageStatus
}

export interface WsUserTyping {
  sender_id: number
}

export interface WsMessageStatus {
  up_to_position: number
  status: MessageStatus
  reader_id: number
}