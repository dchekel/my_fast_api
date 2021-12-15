from typing import Union

from sqlalchemy.orm import Session
from app.v1.crud import CRUDBase
# from app.crud.base import CRUDBase
from app.core.models.models import Category
from app.core.models.models import User
from app.core.schemas.category import CategoryCreate, CategoryUpdate, CategoryUpdateRestricted


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def update(
            self,
            db: Session,
            *,
            db_obj: User,
            obj_in: Union[CategoryUpdate, CategoryUpdateRestricted]
    ) -> Category:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj


category = CRUDCategory(Category)
