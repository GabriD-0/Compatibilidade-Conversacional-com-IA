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
  score: number | null
  classification: AnalysisClassification | null
  last_analysis_at: string | null
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

// ---- Analysis domain ----

export type AnalysisClassification = 'high' | 'mid' | 'low'
export type AnalysisImpact = 'positive' | 'neutral' | 'negative'

export interface AnalysisWarning {
  code: string
  message: string
  participant_id?: number
  [key: string]: unknown
}

export interface AnalysisFactor {
  key: string
  label: string
  score: number
  impact: AnalysisImpact | string
  description: string
}

export interface AnalysisExplanation {
  summary?: string
  factors?: AnalysisFactor[]
  details?: Record<string, unknown>
  [key: string]: unknown
}

export interface AnalysisAggregate {
  score: number
  classification: AnalysisClassification
  weights?: Record<string, number>
  components?: {
    lsm?: number
    sentiment?: number
    behavioral?: number
  }
  warnings?: AnalysisWarning[]
}

export interface AnalysisMetrics {
  lsm?: { score?: number; [key: string]: unknown }
  sentiment?: { score?: number; [key: string]: unknown }
  behavioral?: { score?: number; [key: string]: unknown }
  aggregate?: AnalysisAggregate
  warnings?: AnalysisWarning[]
  [key: string]: unknown
}

export interface ConversationAnalysis {
  id: number
  conversation_id: number
  score: number
  classification: AnalysisClassification
  metrics: AnalysisMetrics
  explanation: AnalysisExplanation
  warnings: AnalysisWarning[]
  message_count: number
  last_message_at: string | null
  computed_at: string | null
}

// ---- Dashboard domain ----

export interface StatValueDash {
  value: number | null
  delta: number | null
}

export interface StatsDash {
  average_score: StatValueDash
  conversations: StatValueDash
  active_pairs: StatValueDash
  analyses_today: StatValueDash
}

export interface WeeklyScoreDash {
  day: string
  score: number | null
  conversations: number
}

export interface ProfileMetricDash {
  metric: string
  value: number
  fullMark: number
}

export interface ScoreDistributionDash {
  range: string
  count: number
}

export interface ClassificationDistributionDash {
  key: AnalysisClassification
  label: string
  value: number
}

export type TrendDash = 'up' | 'down' | 'flat'

export interface TopPairDash {
  conversation_id: number
  a: string
  b: string
  score: number
  trend: TrendDash
}

export interface RecentActivityDash {
  conversation_id: number
  pair: string
  action: string
  score: number | null
  occurred_at: string | null
}

export interface EmotionalPointDash {
  msg: number
  person_a: number | null
  person_b: number | null
}

export interface EmotionalConversationDash {
  conversation_id: number
  label: string
  person_a: string
  person_b: string
  points: EmotionalPointDash[]
}

export interface LsmCategoryDash {
  category: string
  similarity: number
}

export interface BehavioralSignDash {
  conversation_id: number
  pair: string
  latency_minutes: number | null
  balance: number
  message_length_words: number
}

export interface ScatterPointDash {
  conversation_id: number
  pair: string
  lsm: number
  sentiment: number
  score: number
}

export interface SummaryDash {
  stats: StatsDash
  weekly_scores: WeeklyScoreDash[]
  profile: ProfileMetricDash[]
  score_distribution: ScoreDistributionDash[]
  classification_distribution: ClassificationDistributionDash[]
  top_pairs: TopPairDash[]
  recent_activity: RecentActivityDash[]
  emotional_convergence: EmotionalConversationDash[]
  lsm_categories: LsmCategoryDash[]
  behavioral_signs: BehavioralSignDash[]
  scatter: ScatterPointDash[]
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

export type WsAnalysisUpdated = ConversationAnalysis
