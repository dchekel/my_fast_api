# https://fastapi.tiangolo.com/tutorial/bigger-applications/
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.core.models.models import User
from app.core.settings import Session, engine

session = Session(bind=engine)
router = APIRouter(
    prefix="/users",
)


@router.get("/")
async def read_users():
    users = session.query(User).all()  #
    return jsonable_encoder(users)


@router.get("/{u_id}")
async def read_user(u_id: int):
    user = session.query(User).filter(User.id == u_id).first()
    return jsonable_encoder(user)
