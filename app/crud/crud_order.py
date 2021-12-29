from typing import Union

from sqlalchemy.orm import Session
from app.v1.crud import CRUDBase
# from app.crud.base import CRUDBase
from app.core.models.models import Order, User, OrderProduct
from app.core.schemas.order import OrderCreate, OrderUpdateRestricted, OrderUpdate, \
    OrderProduct as OrderProductSchemas, OrderProductCreate, OrderProductUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def update(
            self,
            db: Session,
            *,
            db_obj: Order,
            obj_in: Union[OrderUpdate, OrderUpdateRestricted]
    ) -> Order:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj


order = CRUDOrder(Order)


# class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
class CRUDOrderProduct(CRUDBase[OrderProduct, OrderProductCreate, OrderProductUpdate]):
    def update(
            self,
            db: Session,
            *,
            db_obj: OrderProduct,
            obj_in: Union[OrderProductUpdate, ]
    ) -> OrderProduct:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj


order_product = CRUDOrderProduct(OrderProduct)
