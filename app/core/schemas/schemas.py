# test auth
from typing import Optional
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
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    ...


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    password: str


# Additional properties to return via API
class User(UserInDBBase):
    ...
