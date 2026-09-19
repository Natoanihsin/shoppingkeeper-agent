export interface RetrievedValue {
  value: string
  table_name: string
  column_name: string
  metadata_id: string
  score: number
}

export interface AgentState {
  question: string
  keywords: string[]
  value_candidates: string[]
  retrieved_values: RetrievedValue[]
  retrieved_tables: string[]
  schema_context: string
  retrieval_mode: string
  intent: string
  parameters: Record<string, unknown>
  sql: string | null
  data: Array<Record<string, unknown>>
  answer: string | null
  validation_attempts: number
  error: string | null
}

export interface AgentQueryResult {
  state: AgentState
  requestId: string | null
}

export interface AgentProgressEvent {
  node: string
  message: string
  request_id: string
}

export interface AgentStreamResultEvent {
  state: AgentState
  request_id: string
}

export interface AgentStreamErrorEvent {
  message: string
  request_id?: string
}

export interface AgentStreamCancelledEvent {
  message: string
  request_id: string
}