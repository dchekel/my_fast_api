from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from .order import router as order_router
from .user import router as user_router
from .role import router as role_router

router = APIRouter()

router.include_router(order_router)
router.include_router(user_router)
router.include_router(role_router)


@router.get("/")  # корневая папка
async def read_root():
    title = "Online shop root page"
    return jsonable_encoder(title)


@router.get("/v1")  # корневая папка v1
async def read_root():
    title = "Online shop root page v1"
    return jsonable_encoder(title)


@router.get('/favicon.ico')  # вывод иконки при обращении по адресу 127.0.0.1:8000/
async def favicon():
    file_name = "favicon.ico"
    return FileResponse(file_name)
