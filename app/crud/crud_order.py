from typing import Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.core.models.models import Order, User
from app.core.schemas.order import OrderCreate, OrderUpdateRestricted, OrderUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def update(
            self,
            db: Session,
            *,
            db_obj: User,
            obj_in: Union[OrderUpdate, OrderUpdateRestricted]
    ) -> Order:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj


order = CRUDOrder(Order)

