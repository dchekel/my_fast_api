# https://fastapi.tiangolo.com/tutorial/bigger-applications/
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.core.models.models import Order, User
from app.core.schemas.order import OrderCreate
from app.crud import crud_order
from app.v1.api import get_db, get_current_user

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


'''
@router.post("/", status_code=201, response_model=Order)
def create_order(
    # *,
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Create a new order in the database.
    """
    if order_in.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"You can only submit order as yourself")
    order = crud_order.order.create(db=db, obj_in=order_in)

    return order


end
'''
