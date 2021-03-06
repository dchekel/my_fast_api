from pydantic import BaseModel
from typing import Sequence, Optional


class CategoryBase(BaseModel):
    id: Optional[int]
    name: Optional[str]


class CategoryCreate(CategoryBase):
    # pass
    id: int


class CategoryUpdate(CategoryBase):
    id: int


class CategoryUpdateRestricted(BaseModel):
    id: int
    name: Optional[str]


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass


class CategorySearchResults(BaseModel):
    results: Sequence[Category]
