import {
  Send,
  Square,
} from "lucide-react"
import type {
  FormEvent,
  KeyboardEvent,
} from "react"

interface ComposerProps {
  value: string
  isLoading: boolean
  onChange: (value: string) => void
  onSubmit: () => void
  onCancel: () => void
}

export function Composer({
  value,
  isLoading,
  onChange,
  onSubmit,
  onCancel,
}: ComposerProps) {
  const canSubmit =
    value.trim().length > 0 && !isLoading

  function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    if (canSubmit) {
      onSubmit()
    }
  }

  function handleKeyDown(
    event: KeyboardEvent<HTMLTextAreaElement>,
  ) {
    if (
      event.key === "Enter"
      && !event.shiftKey
      && canSubmit
    ) {
      event.preventDefault()
      onSubmit()
    }
  }

  return (
    <form
      className="composer"
      onSubmit={handleSubmit}
    >
      <label
        className="composer__label"
        htmlFor="question"
      >
        向数据提问
      </label>

      <textarea
        id="question"
        className="composer__input"
        value={value}
        maxLength={500}
        rows={3}
        placeholder="例如：哪个品牌的销售额最高？"
        disabled={isLoading}
        onChange={(event) => {
          onChange(event.target.value)
        }}
        onKeyDown={handleKeyDown}
      />

      <div className="composer__footer">
        <span className="composer__count">
          {value.length}/500
        </span>

        <button
          className={
            isLoading
              ? "composer__submit composer__submit--cancel"
              : "composer__submit"
          }
          type={isLoading ? "button" : "submit"}
          disabled={!isLoading && !canSubmit}
          onClick={isLoading ? onCancel : undefined}
        >
          {isLoading ? (
            <Square
              aria-hidden="true"
              fill="currentColor"
              size={15}
            />
          ) : (
            <Send
              aria-hidden="true"
              size={18}
            />
          )}

          {isLoading ? "停止" : "发送"}
        </button>
      </div>
    </form>
  )
}