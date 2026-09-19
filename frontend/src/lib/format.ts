export function formatCellValue(
  value: unknown,
): string {
  if (value === null || value === undefined) {
    return "-"
  }

  if (typeof value === "number") {
    return new Intl.NumberFormat("zh-CN", {
      maximumFractionDigits: 2,
    }).format(value)
  }

  if (typeof value === "object") {
    return JSON.stringify(value)
  }

  return String(value)
}