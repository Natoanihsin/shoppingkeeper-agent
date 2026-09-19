import { ChartNoAxesCombined } from "lucide-react"

interface EmptyStateProps {
  onSelect: (question: string) => void
}

const suggestions = [
  "哪个品牌的销售额最高？",
  "按月份统计销售额",
  "黄金会员购买了哪些商品？",
]

export function EmptyState({
  onSelect,
}: EmptyStateProps) {
  return (
    <section className="empty-state">
      <ChartNoAxesCombined
        aria-hidden="true"
        size={32}
      />

      <h2>电商数据分析</h2>
      <p>选择一个业务问题开始查询。</p>

      <div className="empty-state__suggestions">
        {suggestions.map((question) => (
          <button
            key={question}
            type="button"
            onClick={() => onSelect(question)}
          >
            {question}
          </button>
        ))}
      </div>
    </section>
  )
}