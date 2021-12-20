# https://fastapi.tiangolo.com/tutorial/bigger-applications/
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.core.models import models
from app.core.schemas.payment import Payment, PaymentUpdateRestricted, PaymentCreate
from app.core.schemas.schemas import User
from app.crud import crud_payment
from app.v1.api import get_db, get_current_active_user, get_current_user

router = APIRouter(prefix="/v1/payments")


@router.get("/", status_code=202, tags=["Get Methods"])
async def get_payments(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Получение всех платежей для аутентифицированного пользователя из базы данных.
    """
    payments = db.query(models.Payment).filter(models.Payment.user_id == current_user.id).all()
    if not payments:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=" This user has no payments",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return jsonable_encoder(payments)


@router.get("/{payment_id}", tags=["Get Methods"])
async def get_payment(
        payment_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Получение платежа по его id для авторизованного пользователя-владельца.
    """
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=" This user has no payments",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_user.id == payment.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This payment belongs to another user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return jsonable_encoder(payment)


@router.post("/", status_code=201, response_model=Payment, tags=["Post Methods"])
def create_payment(
    *,
    payment_in: PaymentCreate,  # Request body Тело запроса проверяется в соответствии с Create pydantic схемой.
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    payment_in.user_id = current_user.id  # TODO неправильно сделано переназначение id пользователя,
    # надо не принимать его в payment_in, но в PaymentCreate оно должно быть??
    """
    Create a new payment in the database. Создание платежа.
    """
    print('router.post create_payment', payment_in.amount, payment_in.user_id, payment_in.order_id)
    payment = crud_payment.payment.create(db=db, obj_in=payment_in)

    return payment


@router.put("/", status_code=201, response_model=Payment, tags=["Put Methods"])
def update_payment(
        *,
        payment_in: PaymentUpdateRestricted,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    Update payment in the database.
    """
    print('router.put update_payment', payment_in.amount, payment_in.id)
    print('payment_in=', payment_in)

    payment = crud_payment.payment.get(db, id=payment_in.id)
    print('payment=', payment.amount, payment.id)
    if not payment:
        raise HTTPException(status_code=400, detail=f"Payment with ID: {payment_in.id} not found.")

    if payment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"You can only update your payments.")

    updated_payment = crud_payment.payment.update(db=db, db_obj=payment, obj_in=payment_in)

    print('updated_payment=', updated_payment)
    return updated_payment


@router.delete('/delete/{payment_id}/', status_code=201, response_model=Payment, tags=["Delete Methods"])
async def delete_payment(
        *,
        payment_in: PaymentUpdateRestricted,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user),
):

    """
      Delete payment from database. Это пример удаления. На практике удалять может только суперюзер.
    """
    payment = crud_payment.payment.get(db, id=payment_in.id)
    if payment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"You can only delete your payments.")
    deleted_payment = crud_payment.payment.remove(db=db, id=payment_in.id)

    return deleted_payment
