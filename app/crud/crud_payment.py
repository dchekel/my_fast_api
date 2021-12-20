from typing import Union

from sqlalchemy.orm import Session
from app.v1.crud import CRUDBase
from app.core.models.models import User, Payment
from app.core.schemas.payment import PaymentCreate, PaymentUpdateRestricted, PaymentUpdate


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    def update(
            self,
            db: Session,
            *,
            db_obj: User,
            obj_in: Union[PaymentUpdate, PaymentUpdateRestricted]
    ) -> Payment:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj


payment = CRUDPayment(Payment)

