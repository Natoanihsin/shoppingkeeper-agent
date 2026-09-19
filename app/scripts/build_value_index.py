from uuid import NAMESPACE_URL, uuid5

from elasticsearch.helpers import bulk

from app.clients.elasticsearch_client import elasticsearch_client
from app.core.config import get_settings
from app.db.connection import run_sql

settings = get_settings()

VALUE_FIELDS = [
    ("dim_region", "province", "column_dim_region_province"),
    ("dim_region", "region_name", "column_dim_region_region_name"),
    ("dim_region", "country", "column_dim_region_country"),
    ("dim_customer", "customer_name", "column_dim_customer_customer_name"),
    ("dim_customer", "gender", "column_dim_customer_gender"),
    ("dim_customer", "member_level", "column_dim_customer_member_level"),
    ("dim_product", "product_name", "column_dim_product_product_name"),
    ("dim_product", "category", "column_dim_product_category"),
    ("dim_product", "brand", "column_dim_product_brand"),
    ("dim_date", "full_date", "column_dim_date_full_date"),
]


def load_distinct_values(
    table_name: str,
    column_name: str,
) -> list[str]:
    sql = f"""
        SELECT DISTINCT `{column_name}` AS value
        FROM `{table_name}`
        WHERE `{column_name}` IS NOT NULL
    """

    rows = run_sql(sql)

    return [
        str(row["value"])
        for row in rows
    ]


def build_actions() -> list[dict]:
    actions: list[dict] = []

    for table_name, column_name, metadata_id in VALUE_FIELDS:
        values = load_distinct_values(
            table_name,
            column_name,
        )

        for value in values:
            document_id = str(
                uuid5(
                    NAMESPACE_URL,
                    f"{table_name}:{column_name}:{value}",
                )
            )

            actions.append(
                {
                    "_index": settings.elasticsearch_value_index,
                    "_id": document_id,
                    "_source": {
                        "value": value,
                        "table_name": table_name,
                        "column_name": column_name,
                        "metadata_id": metadata_id,
                    },
                }
            )

    return actions


def main() -> None:
    actions = build_actions()

    success_count, _ = bulk(
        elasticsearch_client,
        actions,
        refresh=True,
    )

    print(f"Indexed field values: {success_count}")


if __name__ == "__main__":
    main()