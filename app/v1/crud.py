from app.core.models.models import User
from app.core.schemas.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash


from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import as_declarative, declared_attr
# from app.db.base_class import Base
import typing


class_registry: typing.Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: typing.Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 5000
    ) -> List[ModelType]:
        return (
            db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    '''
    Важно отметить, что в этом create методе (обратите внимание, что мы переопределяем родительский CRUDBase метод) 
    мы конвертируем модель Pydantic в словарь, вызывая, obj_in.dict() а затем удаляя password запись из словаря с помощью 
    .pop(). Затем, чтобы сгенерировать хешированный пароль, мы вызываем новый метод get_password_hash.
    '''
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        print('obj_in= ', obj_in, '       password', obj_in.password)
        create_data = obj_in.dict()
        print('create_data before pop= ', create_data)
        create_data.pop("password")
        print('create_data= ', create_data)
        db_obj = User(**create_data)
        print('db_obj= ', db_obj)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db_obj.password = db_obj.hashed_password
        db_obj.address = ''
        print('db_obj.hashed_password= ', db_obj.hashed_password)

        db.add(db_obj)  # не хватает поля hashed_password в объекте db=session
        db.commit()

        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
