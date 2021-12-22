from pydantic import BaseModel
from datetime import datetime
# from typing import Sequence


class OrderBase(BaseModel):
    user_id: int
    status_id: int
    total_cost: float
    total_quantity: float


class OrderCreate(BaseModel):
    id: int
    user_id: int
    status_id: int
    total_cost: float
    total_quantity: float
    created_at: datetime


class OrderUpdate(OrderBase):
    status_id: int
    closed_at: datetime


class OrderUpdateRestricted(BaseModel):
    id: int


# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Order(OrderInDBBase):
    pass


'''

# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    id: int
    submitter_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Order(OrderInDBBase):
    pass


# Properties properties stored in DB
class OrderInDB(OrderInDBBase):
    pass


class OrderSearchResults(BaseModel):
    results: Sequence[Order]
'''
