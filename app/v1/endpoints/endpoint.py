from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from .order import router as order_router
from .user import router as user_router

# session = Session(bind=engine)
router = APIRouter()

router.include_router(order_router)
router.include_router(user_router)


@router.get("/")  # корневая папка
async def read_root():
    title = "Online shop root page"
    return jsonable_encoder(title)


@router.get("/v1")  # корневая папка v1
async def read_root():
    title = "Online shop root page v1"
    return jsonable_encoder(title)
