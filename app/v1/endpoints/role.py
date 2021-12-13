from typing import Any
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.core.models.models import Role
from app.v1.api import get_db

router = APIRouter(prefix="/v1/roles")


@router.get("/", status_code=202)
async def get_roles(
        db: Session = Depends(get_db)
) -> Any:
    roles = db.query(Role).all()  # session.query(Order).all()
    return jsonable_encoder(roles)


@router.get("/{role_id}")
async def get_role(
        role_id: int,
        db: Session = Depends(get_db)
) -> Any:
    role = db.query(Role).filter(Role.id == role_id).first()
    return jsonable_encoder(role)
