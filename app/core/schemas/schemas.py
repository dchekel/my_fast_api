# test auth
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class AuthDetails(BaseModel):
    username: str
    password: str


# new part from part-10
class UserBase(BaseModel):
    username: Optional[str]  # ?
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str  # пароль нужен только при создании пользователя


# Properties to receive via API on update
class UserUpdate(UserBase):
    ...


class Role(BaseModel):
    id: int
    name: str

    class Config:  # иначе -  value is not a valid dict (type=type_error.dict)
        orm_mode = True


class UserInDBBase(UserBase):
    id: Optional[int] = None
    # relationship  this from app/core/models/models.py class User(Base):
    # roles = relationship("Role",
    #                      secondary=association_table_user_role,  # многие-ко-многим
    #                      back_populates="users")
    roles: List[Role] = []

    class Config:  # иначе -  value is not a valid dict (type=type_error.dict)
        orm_mode = True  # SQLAlchemy не возвращает словарь, чего ожидает pydantic по умолчанию


# Additional properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    password: str


# Additional properties to return via API
class User(UserInDBBase):
    ...

