# https://fastapi.tiangolo.com/tutorial/bigger-applications/
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.core.models.models import Order, User
from app.core.schemas.order import OrderCreate, Order as OrderSchemas
# from app.core.schemas.order import Order as OrderSchemas
from app.core.schemas import schemas
from app.crud import crud_order
from app.v1.api import get_db, get_current_user, get_current_active_user

router = APIRouter(prefix="/v1/orders")


@router.get("/", status_code=202, tags=["Get Methods"])
async def get_orders(
        db: Session = Depends(get_db),
        current_user: schemas.User =Depends(get_current_active_user)
) -> Any:
    """
    Получение всех заказов для аутентифицированного пользователя из базы данных.
    """
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()  # session.query(Order).all()
    return jsonable_encoder(orders)


@router.get("/{order_id}", tags=["Get Methods"])
async def get_order(
        order_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User =Depends(get_current_active_user)
) -> Any:
    """
    Получение заказа по его id для авторизованного пользователя-владельца.
    """
    order = db.query(Order).filter(Order.id == order_id).first()

    if not current_user.id == order.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This order belongs to another user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return jsonable_encoder(order)


@router.post("/", status_code=201, response_model=OrderSchemas, tags=["Post Methods"])  #
def create_order(
    # *,
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    Create a new order in the database.
    """
    print('from @router.post create_order', '\norder_in = ', order_in)
    if order_in.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"You can only submit order as yourself")
    order = crud_order.order.create(db=db, obj_in=order_in)

    return order


'''
'''