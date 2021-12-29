from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class OrderProduct(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: float
    price: float

    class Config:  # иначе -  value is not a valid dict (type=type_error.dict)
        orm_mode = True


class OrderProductCreate(BaseModel):
    # pass
    # id: int
    order_id: int
    product_id: int
    quantity: float
    price: float

    class Config:
        orm_mode = True


class OrderProductUpdate(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: float
    price: float


class OrderBase(BaseModel):
    user_id: int
    status_id: int
    total_cost: float
    total_quantity: float
    order_product: Optional[List[OrderProduct]] = None  # https://fastapi.tiangolo.com/tutorial/body-nested-models/


class OrderCreate(BaseModel):
    pass
    # id: int
    # user_id: int
    # status_id: int
    # total_cost: float
    # total_quantity: float
    # created_at: datetime
    # order_product: Optional[List[OrderProduct]] = None
    # было при отладке: при наличии, выдает ошибку,  TypeError: 'products' is an invalid keyword argument for Order

    # class Config:
    #     orm_mode = True


class OrderUpdateRestricted(BaseModel):
    id: int


class OrderUpdate(OrderUpdateRestricted):
    status_id: int
    closed_at: datetime


# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    id: int
    user_id: int
    order_product: Optional[List[OrderProduct]] = None  # https://fastapi.tiangolo.com/tutorial/body-nested-models/

    class Config:
        orm_mode = True


# Properties to return to client
class Order(OrderInDBBase):
    # pass
    order_product: Optional[List[OrderProduct]] = None  # https://fastapi.tiangolo.com/tutorial/body-nested-models/

    class Config:
        orm_mode = True


'''

# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    id: int
    submitter_id: int

    class Config:
        orm_mode = True


# Properties properties stored in DB
class OrderInDB(OrderInDBBase):
    pass


class OrderSearchResults(BaseModel):
    results: Sequence[Order]
'''
