import { io, type Socket } from 'socket.io-client'
import type { WsNewMessage, WsUserTyping, WsMessageStatus } from '../types/types'

const ACCESS_KEY = 'access_token'

let socket: Socket | null = null

function getSocket(): Socket {
  if (!socket) {
    socket = io(import.meta.env.VITE_API_BASE_URL as string, {
      autoConnect: false,
      transports: ['websocket'],
    })
  }
  return socket
}

export function connectSocket(): void {
  const socket = getSocket()
  socket.auth = { token: localStorage.getItem(ACCESS_KEY) ?? '' }
  if (!socket.connected) socket.connect()
}

export function disconnectSocket(): void {
  socket?.disconnect()
}

export function joinConversation(id: number): Promise<{ ok: true }> {
  return getSocket().emitWithAck('join', { conversation_id: id })
}

export function leaveConversation(id: number): void {
  getSocket().emit('leave', { conversation_id: id })
}

export function sendMessage(conversationId: number, content: string): Promise<{ ok: true; position: number }> {
  return getSocket().emitWithAck('send_message', { conversation_id: conversationId, content })
}

export function emitTyping(conversationId: number): void {
  getSocket().emit('typing', { conversation_id: conversationId })
}

export function emitRead(conversationId: number, upToPosition: number): void {
  getSocket().emit('read', { conversation_id: conversationId, up_to_position: upToPosition })
}

export function onNewMessage(handler: (data: WsNewMessage) => void): () => void {
  const socket = getSocket()
  socket.on('new_message', handler)
  return () => socket.off('new_message', handler)
}

export function onUserTyping(handler: (data: WsUserTyping) => void): () => void {
  const socket = getSocket()
  socket.on('user_typing', handler)
  return () => socket.off('user_typing', handler)
}

export function onMessageStatus(handler: (data: WsMessageStatus) => void): () => void {
  const socket = getSocket()
  socket.on('message_status', handler)
  return () => socket.off('message_status', handler)
}
