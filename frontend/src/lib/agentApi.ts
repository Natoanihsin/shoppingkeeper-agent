import type {
    AgentStreamCancelledEvent,
  AgentProgressEvent,
  AgentQueryResult,
  AgentState,
  AgentStreamErrorEvent,
  AgentStreamResultEvent,
} from "../types/agent"

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  "http://127.0.0.1:8000"

interface ParsedSseEvent {
  event: string
  data: unknown
}

export interface AgentStreamHandlers {
  onStarted?: (requestId: string | null) => void
  onProgress: (event: AgentProgressEvent) => void
  onResult: (result: AgentQueryResult) => void
}

function parseSseEvent(
  block: string,
): ParsedSseEvent | null {
  let event = "message"
  const dataLines: string[] = []

  for (const line of block.split(/\r?\n/)) {
    if (line.startsWith("event:")) {
      event = line.slice(6).trim()
    }

    if (line.startsWith("data:")) {
      dataLines.push(line.slice(5).trimStart())
    }
  }

  if (dataLines.length === 0) {
    return null
  }

  const data: unknown = JSON.parse(
    dataLines.join("\n"),
  )

  return {
    event,
    data,
  }
}

export async function queryAgent(
  question: string,
): Promise<AgentQueryResult> {
  const response = await fetch(`${API_BASE_URL}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
    }),
  })

  const requestId = response.headers.get("X-Request-ID")

  if (!response.ok) {
    const errorBody = await response.text()

    throw new Error(
      `Request failed (${response.status}): ${errorBody}`,
    )
  }

  const state = (await response.json()) as AgentState

  return {
    state,
    requestId,
  }
}

export async function streamQueryAgent(
  question: string,
  handlers: AgentStreamHandlers,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/query/stream`,
    {
      signal,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
      }),
    },
  )

  if (!response.ok) {
    const errorBody = await response.text()

    throw new Error(
      `Request failed (${response.status}): ${errorBody}`,
    )
  }

  handlers.onStarted?.(
  response.headers.get("X-Request-ID"),
  )

  if (!response.body) {
    throw new Error("浏览器没有返回可读取的数据流。")
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ""
  let receivedResult = false

  function dispatchBlock(block: string) {
    const parsed = parseSseEvent(block)

    if (!parsed) {
      return
    }

    if (parsed.event === "progress") {
      handlers.onProgress(
        parsed.data as AgentProgressEvent,
      )
      return
    }

    if (parsed.event === "result") {
      const result =
        parsed.data as AgentStreamResultEvent

      receivedResult = true
      handlers.onResult({
        state: result.state,
        requestId: result.request_id,
      })
      return
    }

    if (parsed.event === "cancelled") {
  const cancelled =
    parsed.data as AgentStreamCancelledEvent

  throw new DOMException(
    cancelled.message,
    "AbortError",
  )
}

    if (parsed.event === "error") {
      const error =
        parsed.data as AgentStreamErrorEvent

      throw new Error(error.message)
    }
  }

  function cancelReader() {
    void reader.cancel("Query cancelled")
  }

  signal?.addEventListener(
    "abort",
    cancelReader,
    { once: true },
  )

  try {
    while (true) {
      const { done, value } = await reader.read()

      if (done) {
        break
      }

      buffer += decoder.decode(value, {
        stream: true,
      })

      const blocks = buffer.split(/\r?\n\r?\n/)
      buffer = blocks.pop() ?? ""

      for (const block of blocks) {
        dispatchBlock(block)
      }
    }

    if (signal?.aborted) {
      throw new DOMException(
        "Query cancelled",
        "AbortError",
      )
    }

    buffer += decoder.decode()

    if (buffer.trim()) {
      dispatchBlock(buffer)
    }

    if (!receivedResult) {
      throw new Error(
        "数据流已经结束，但没有收到查询结果。",
      )
    }
  } finally {
    signal?.removeEventListener(
      "abort",
      cancelReader,
    )
    reader.releaseLock()
  }
}

export async function cancelAgentQuery(
  requestId: string,
): Promise<boolean> {
  const encodedRequestId =
    encodeURIComponent(requestId)

  const response = await fetch(
    `${API_BASE_URL}/query/cancel/${encodedRequestId}`,
    {
      method: "POST",
    },
  )

  if (!response.ok) {
    const errorBody = await response.text()

    throw new Error(
      `Cancel request failed `
      + `(${response.status}): ${errorBody}`,
    )
  }

  const result = (await response.json()) as {
    request_id: string
    cancelled: boolean
  }

  return result.cancelled
}