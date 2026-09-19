import { formatCellValue } from "../lib/format"

interface ResultTableProps {
  rows: Array<Record<string, unknown>>
}

export function ResultTable({
  rows,
}: ResultTableProps) {
  if (rows.length === 0) {
    return null
  }

  const columns = Array.from(
    new Set(
      rows.flatMap((row) => Object.keys(row)),
    ),
  )

  return (
    <div className="result-table__scroll">
      <table className="result-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>
                {column}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((column) => (
                <td key={column}>
                  {formatCellValue(row[column])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}