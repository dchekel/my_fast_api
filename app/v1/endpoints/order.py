# https://fastapi.tiangolo.com/tutorial/bigger-applications/
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.core.models.models import Order
from app.core.settings import Session, engine

session = Session(bind=engine)
router = APIRouter(
    prefix="/orders",
)


@router.get("/")
async def get_orders():
    orders = session.query(Order).all()  #
    return jsonable_encoder(orders)


@router.get("/{o_id}")
async def get_order(o_id: int):
    order = session.query(Order).filter(Order.id == o_id).first()
    return jsonable_encoder(order)
