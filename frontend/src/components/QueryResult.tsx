import {
  AlertTriangle,
  CheckCircle2,
  Code2,
  Database,
} from "lucide-react"

import type {
  AgentQueryResult,
} from "../types/agent"
import { ResultTable } from "./ResultTable"

interface QueryResultProps {
  result: AgentQueryResult
}

export function QueryResult({
  result,
}: QueryResultProps) {
  const { state, requestId } = result

  return (
    <section
      className="query-result"
      aria-live="polite"
    >
      <header className="query-result__header">
        {state.error ? (
          <AlertTriangle
            aria-hidden="true"
            size={22}
          />
        ) : (
          <CheckCircle2
            aria-hidden="true"
            size={22}
          />
        )}

        <div>
          <h2>查询结果</h2>
          <p>{state.answer ?? "查询已完成。"}</p>
        </div>
      </header>

      <dl className="query-result__meta">
        <div>
          <dt>意图</dt>
          <dd>{state.intent}</dd>
        </div>

        <div>
          <dt>检索方式</dt>
          <dd>{state.retrieval_mode}</dd>
        </div>

        <div>
          <dt>相关表</dt>
          <dd>
            {state.retrieved_tables.length > 0
              ? state.retrieved_tables.join(", ")
              : "直接查询"}
          </dd>
        </div>

        <div>
          <dt>SQL 校验</dt>
          <dd>{state.validation_attempts} 次</dd>
        </div>
      </dl>

      {state.data.length > 0 && (
        <section className="query-result__data">
          <h3>
            <Database
              aria-hidden="true"
              size={18}
            />
            数据
          </h3>

          <ResultTable rows={state.data} />
        </section>
      )}

      {state.sql && (
        <details className="query-result__sql">
          <summary>
            <Code2
              aria-hidden="true"
              size={18}
            />
            查看 SQL
          </summary>

          <pre>
            <code>{state.sql}</code>
          </pre>
        </details>
      )}

      {requestId && (
        <footer className="query-result__footer">
          Request ID: <code>{requestId}</code>
        </footer>
      )}
    </section>
  )
}