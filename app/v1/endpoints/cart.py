# https://fastapi.tiangolo.com/tutorial/bigger-applications/
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.core.models.models import Cart as model_Cart, User
from app.core.schemas.cart import Cart, CartCreate
# from app.core.schemas.order import Order as OrderSchemas
from app.core.schemas import schemas
from app.crud import crud_cart
from app.v1.api import get_db, get_current_user, get_current_active_user

router = APIRouter(prefix="/v1/cart")


@router.get("/", status_code=202, tags=["Get Methods"])
async def get_cart(
        db: Session = Depends(get_db),
        current_user: schemas.User =Depends(get_current_active_user)
) -> Any:
    """
    Получение корзины аутентифицированного пользователя из базы данных.
    """
    cart = db.query(model_Cart).filter(model_Cart.user_id == current_user.id).all()  # session.query(Order).all()
    return jsonable_encoder(cart)


@router.post("/", status_code=201, response_model=Cart, tags=["Post Methods"])  #
def filling_cart(
    # *,
    cart_in: CartCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
     filling the user's shopping cart in the database. Наполнение корзины товаров пользователя
    """
    print('from @router.post filling_cart', '\ncart_in = ', cart_in)
    cart_in.user_id = current_user.id
    # if cart_in.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail=f"You can only append to cart as yourself")
    cart = crud_cart.cart.create(db=db, obj_in=cart_in)

    return cart


'''
'''