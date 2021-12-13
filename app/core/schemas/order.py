from pydantic import BaseModel, HttpUrl

# from typing import Sequence


class OrderBase(BaseModel):
    id: int
    # total_cost: float
    # label: str
    # source: str
    # url: HttpUrl


class OrderCreate(OrderBase):
    user_id: int
    # label: str
    # source: str
    # url: HttpUrl


class OrderUpdate(OrderBase):
    id: int


class OrderUpdateRestricted(BaseModel):
    id: int
    # label: str
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
