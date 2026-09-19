import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError

ALLOWED_TABLES = {
    "fact_order",
    "dim_region",
    "dim_customer",
    "dim_product",
    "dim_date",
}

BLOCKED_FUNCTIONS = {
    "SLEEP",
    "BENCHMARK",
    "LOAD_FILE",
}

MAX_ROWS = 200

class SQLValidationError(ValueError):
    pass


def validate_read_only_sql(sql: str) -> str:
    if not sql or not sql.strip():
        raise SQLValidationError("SQL 不能为空")

    try:
        statements = sqlglot.parse(
            sql.strip(),
            read="mysql",
        )
    except ParseError as exc:
        raise SQLValidationError(f"SQL 无法解析：{exc}") from exc

    if len(statements) != 1:
        raise SQLValidationError("一次只允许执行一条 SQL")

    statement = statements[0]

    if not isinstance(statement, exp.Query):
        raise SQLValidationError("只允许执行只读查询")

    unsafe_types = (
        exp.DML,
        exp.DDL,
        exp.Command,
        exp.Into,
        exp.Lock,
    )

    for node in statement.walk():
        if isinstance(node, unsafe_types):
            operation = type(node).__name__
            raise SQLValidationError(f"检测到不允许的 SQL 操作：{operation}")

        if isinstance(node, exp.Anonymous):
            function_name = node.name.upper()

            if function_name in BLOCKED_FUNCTIONS:
                raise SQLValidationError(
                    f"检测到不允许的函数：{function_name}"
                )

    for table in statement.find_all(exp.Table):
        table_name = table.name.lower()

        if table_name not in ALLOWED_TABLES:
            raise SQLValidationError(
                f"表不在允许范围内：{table.name}"
            )

    limit = statement.args.get("limit")

    if limit is None:
        statement = statement.limit(MAX_ROWS)
    else:
        limit_value = limit.expression

        if not isinstance(limit_value, exp.Literal) or not limit_value.is_int:
            raise SQLValidationError("LIMIT 必须是整数")

        if int(limit_value.this) > MAX_ROWS:
            statement = statement.limit(MAX_ROWS)

    return statement.sql(dialect="mysql")