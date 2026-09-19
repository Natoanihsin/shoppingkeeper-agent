from app.db.connection import run_sql


def get_order_count() -> int:
    rows = run_sql("SELECT COUNT(*) AS order_count FROM fact_order")
    return rows[0]["order_count"]


def get_total_sales() -> float:
    rows = run_sql("SELECT SUM(order_amount) AS total_sales FROM fact_order")
    return float(rows[0]["total_sales"])