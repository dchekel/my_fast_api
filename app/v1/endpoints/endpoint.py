from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.core.settings import Session, engine

# session = Session(bind=engine)
router = APIRouter()


@router.get("/")  # корневая папка
async def read_root():
    title = "Online shop root page"
    return jsonable_encoder(title)
