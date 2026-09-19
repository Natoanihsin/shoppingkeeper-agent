import { DatabaseZap } from "lucide-react"
import {
  useRef,
  useState,
} from "react"

import { Composer } from "./components/Composer"
import { EmptyState } from "./components/EmptyState"
import { LoadingState } from "./components/LoadingState"
import { QueryResult } from "./components/QueryResult"
import {
  cancelAgentQuery,
  streamQueryAgent,
} from "./lib/agentApi"
import type {
  AgentProgressEvent,
  AgentQueryResult,
} from "./types/agent"

function App() {
  const [question, setQuestion] = useState("")
  const [result, setResult] =
    useState<AgentQueryResult | null>(null)
  const [progressEvents, setProgressEvents] =
    useState<AgentProgressEvent[]>([])
  const [error, setError] =
    useState<string | null>(null)
  const [isLoading, setIsLoading] =
    useState(false)

  const activeRequest =
    useRef<AbortController | null>(null)
  const activeRequestId =
    useRef<string | null>(null)

  async function runQuery(nextQuestion: string) {
    const normalizedQuestion = nextQuestion.trim()

    if (!normalizedQuestion || isLoading) {
      return
    }

    setQuestion(normalizedQuestion)
    setResult(null)
    setProgressEvents([])
    setError(null)
    setIsLoading(true)

    const controller = new AbortController()

    activeRequest.current = controller
    activeRequestId.current = null

    try {
      await streamQueryAgent(
        normalizedQuestion,
        {
          onStarted(requestId) {
            activeRequestId.current = requestId
          },

          onProgress(event) {
            if (controller.signal.aborted) {
              return
            }

            setProgressEvents((currentEvents) => [
              ...currentEvents,
              event,
            ])
          },

          onResult(nextResult) {
            if (controller.signal.aborted) {
              return
            }

            setError(null)
            setResult(nextResult)
          },
        },
        controller.signal,
      )
    } catch (requestError) {
      const wasCancelled =
        requestError instanceof DOMException
        && requestError.name === "AbortError"

      const message = wasCancelled
        ? "查询已停止。"
        : requestError instanceof Error
          ? requestError.message
          : "查询失败，请稍后重试。"

      setError(message)
    } finally {
      if (activeRequest.current === controller) {
        activeRequest.current = null
        activeRequestId.current = null
      }

      setIsLoading(false)
    }
  }

  function cancelQuery() {
    const requestId = activeRequestId.current

    if (!requestId) {
      activeRequest.current?.abort()
      setError("查询已停止。")
      setIsLoading(false)
      return
    }

    setError("正在停止查询，请稍候……")

    void cancelAgentQuery(requestId)
      .then((cancelled) => {
        if (!cancelled) {
          setError("查询已经结束，无需停止。")
        }
      })
      .catch((cancelError: unknown) => {
        const message =
          cancelError instanceof Error
            ? cancelError.message
            : "停止请求发送失败。"

        setError(
          `停止请求发送失败，查询仍在运行：${message}`,
        )
      })
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <DatabaseZap
          aria-hidden="true"
          size={28}
        />

        <div>
          <strong>Shopkeeper Agent</strong>
          <span>电商问数工作台</span>
        </div>
      </header>

      <main className="workspace">
        <section className="query-panel">
          <h1>数据查询</h1>

          <Composer
            value={question}
            isLoading={isLoading}
            onChange={setQuestion}
            onSubmit={() => {
              void runQuery(question)
            }}
            onCancel={cancelQuery}
          />

          {error && (
            <p
              className="query-panel__error"
              role="alert"
            >
              {error}
            </p>
          )}
        </section>

        <section className="result-panel">
          {isLoading ? (
            <LoadingState events={progressEvents} />
          ) : result ? (
            <QueryResult result={result} />
          ) : (
            <EmptyState
              onSelect={(suggestion) => {
                void runQuery(suggestion)
              }}
            />
          )}
        </section>
      </main>
    </div>
  )
}

export default App