from fastapi import APIRouter

from app.services.order_service import get_order_count, get_total_sales

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/count")
def order_count() -> dict[str, int]:
    return {"order_count": get_order_count()}


@router.get("/total-sales")
def total_sales() -> dict[str, float]:
    return {"total_sales": get_total_sales()}