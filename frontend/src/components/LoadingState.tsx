import {
  CheckCircle2,
  LoaderCircle,
} from "lucide-react"

import type {
  AgentProgressEvent,
} from "../types/agent"

interface LoadingStateProps {
  events: AgentProgressEvent[]
}

export function LoadingState({
  events,
}: LoadingStateProps) {
  const currentMessage =
    events.at(-1)?.message ?? "正在准备查询"
  const visibleEvents = events.slice(-6)

  return (
    <section
      className="loading-state"
      aria-live="polite"
      aria-busy="true"
    >
      <LoaderCircle
        aria-hidden="true"
        className="loading-state__spinner"
        size={34}
      />

      <h2>{currentMessage}</h2>
      <p>Agent 正在继续执行后续步骤。</p>

      {visibleEvents.length > 0 && (
        <ol className="loading-state__progress">
          {visibleEvents.map((event, index) => (
            <li key={`${event.node}-${index}`}>
              <CheckCircle2
                aria-hidden="true"
                size={16}
              />
              <span>{event.message}</span>
            </li>
          ))}
        </ol>
      )}
    </section>
  )
}