import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from app.db.connection import engine


@pytest.mark.integration
def test_readonly_user_can_select() -> None:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM fact_order")
        )

        assert result.scalar_one() >= 0


@pytest.mark.integration
def test_readonly_user_cannot_update() -> None:
    with pytest.raises(DBAPIError):
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    UPDATE dim_product
                    SET product_name = product_name
                    WHERE product_id = -1
                    """
                )
            )