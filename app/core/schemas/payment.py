from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentBase(BaseModel):
    id: int
    amount: Optional[float]
    # paid_at: str
    order_id: int
    # user_id: int


class PaymentCreate(BaseModel):
    user_id: Optional[int]
    order_id: int
    amount: Optional[float]
    paid_at: datetime


class PaymentUpdate(PaymentBase):
    id: int


class PaymentUpdateRestricted(PaymentBase):  # BaseModel
    # id: int
    user_id: int
    # amount: Optional[float]


# Properties shared by models stored in DB
class PaymentInDBBase(PaymentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Payment(PaymentInDBBase):
    pass


# Properties stored in DB
class OrderInDB(PaymentInDBBase):
    pass
