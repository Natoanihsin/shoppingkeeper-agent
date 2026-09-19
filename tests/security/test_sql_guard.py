import pytest

from app.security.sql_guard import SQLValidationError, validate_read_only_sql


def  test_allows_select_query() -> None:
    sql = validate_read_only_sql("SELECT * FROM fact_order")

    assert sql == "SELECT * FROM fact_order LIMIT 200"

def test_allows_parameter_placeholder() -> None:
    sql = validate_read_only_sql(
        "SELECT * FROM dim_region WHERE region_name = :region_name"
    )

    assert ":region_name" in sql


def test_rejects_delete_query() -> None:
    with pytest.raises(SQLValidationError, match="只允许执行只读查询"):
        validate_read_only_sql("DELETE FROM fact_order")


def test_rejects_multiple_statements() -> None:
    with pytest.raises(SQLValidationError, match="一次只允许执行一条 SQL"):
        validate_read_only_sql(
            "SELECT * FROM fact_order; DELETE FROM fact_order"
        )


def test_rejects_empty_sql() -> None:
    with pytest.raises(SQLValidationError, match="SQL 不能为空"):
        validate_read_only_sql("")

def test_rejects_unknown_table() -> None:
    with pytest.raises(SQLValidationError, match="表不在允许范围内"):
        validate_read_only_sql("SELECT * FROM mysql.user")


def test_rejects_blocked_function() -> None:
    with pytest.raises(SQLValidationError, match="检测到不允许的函数"):
        validate_read_only_sql("SELECT SLEEP(5)")

def test_keeps_small_limit() -> None:
    sql = validate_read_only_sql(
        "SELECT * FROM fact_order LIMIT 20"
    )

    assert sql.endswith("LIMIT 20")


def test_caps_large_limit() -> None:
    sql = validate_read_only_sql(
        "SELECT * FROM fact_order LIMIT 1000"
    )

    assert sql.endswith("LIMIT 200")