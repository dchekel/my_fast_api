# https://fastapi.tiangolo.com/tutorial/bigger-applications/
from typing import Any
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.core.models.models import Order
from app.v1.api import get_db

router = APIRouter(prefix="/v1/orders")


@router.get("/", status_code=202)
async def get_orders(
        db: Session = Depends(get_db)
) -> Any:
    orders = db.query(Order).all()  # session.query(Order).all()
    return jsonable_encoder(orders)


@router.get("/{o_id}")
async def get_order(
        o_id: int,
        db: Session = Depends(get_db)
) -> Any:
    order = db.query(Order).filter(Order.id == o_id).first()
    return jsonable_encoder(order)
