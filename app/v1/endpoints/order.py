# https://fastapi.tiangolo.com/tutorial/bigger-applications/

from datetime import datetime
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.core.models.models import Order, OrderProduct, User
from app.core.schemas.order import OrderCreate, Order as OrderSchemas, OrderUpdate, OrderUpdateRestricted, \
    OrderProductCreate as OrderProductCreateScheme, OrderProduct as OrderProductScheme
from app.core.schemas.cart import Cart
# from app.core.schemas.order import Order as OrderSchemas
from app.core.schemas import schemas
from app.crud import crud_order
from app.v1.api import get_db, get_current_user, get_current_active_user, get_cart_current_user

router = APIRouter(prefix="/v1/orders")


@router.get("/", status_code=202, tags=["Get Methods"])
async def get_orders(
        db: Session = Depends(get_db),
        current_user: schemas.User =Depends(get_current_active_user)
) -> Any:
    """
    Получение всех заказов для аутентифицированного пользователя из базы данных.
    """
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()  # session.query(Order).all()
    return jsonable_encoder(orders)


@router.get("/{order_id}", response_model=OrderSchemas, tags=["Get Methods"])
async def get_order(
        order_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User =Depends(get_current_active_user)
) -> Any:
    """
    Получение заказа по его id для авторизованного пользователя-владельца.
    """
    order = db.query(Order).filter(Order.id == order_id).first()

    if not current_user.id == order.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This order belongs to another user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return jsonable_encoder(order)


@router.post("/", status_code=201, response_model=OrderSchemas, tags=["Post Methods"])  #
def create_order(
        order_in: OrderCreate,  # order_product_scheme: OrderProductScheme,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user),
        cart_in: Cart = Depends(get_cart_current_user),  # TODO разобраться, почему схема Cart принимает модель Cart
)-> dict:
    """
    Create a new order in the database. Transferring the contents of the cart to the order.
    """
    #  TODO надо убрать из request_body все поля: user_id и взять из  current_user.id, products и взять из корзины ...
    # if order_in.user_id != current_user.id:
    if not current_user:
        raise HTTPException(status_code=403, detail=f"You are not authorized.")

    # print('from @router.post create_order', '\n order_in = ', type(order_in), order_in)
    # order_in = <class 'app.core.schemas.order.OrderCreate'>
    # id=31 user_id=1 status_id=1 total_cost=200.0 total_quantity=2.0
    # created_at=datetime.datetime(2021, 12, 28, 6, 54, 9, 905000, tzinfo=datetime.timezone.utc) products=[]

    # print('from @router.post create_order', '\n cart_in = ', type(cart_in), cart_in)
    # cart_in =  <class 'list'>  # список экземпляров класса Cart
    # [<app.core.models.models.Cart object at 0x7fd4dfe6d490>,
    # <app.core.models.models.Cart object at 0x7fd4dfe6d400>,
    # <app.core.models.models.Cart object at 0x7fd4dfe6d520>,
    # <app.core.models.models.Cart object at 0x7fd4dfe6d580>,
    # <app.core.models.models.Cart object at 0x7fd4dfe6d5e0>]

    # print('from @router.post create_order', '\n экземпляр класса Cart = ', type(cart_in[0]), cart_in[0])
    # id: int  user_id: int status_id: int
    order_data = order_in.dict()
    order_data['user_id'] = current_user.id  # id юзера берем из id текущего аутентифицированного пользователя
    order_data['status_id'] = 1  # присваиваем статус заказа 'создан', соответствующий 1
    order_data['created_at'] = datetime.now()

    # modified_product_data = order_data.pop('order_product', None)  # убираем из экз.класса OrderCreate список с продукцией OrderProduct
    #  order_product=[]  из order_data(order_in)
    print('from @router.post create_order', '\norder_data = ', type(order_data), order_data)
    # print('from @router.post create_order', '\nmodified_product_data = ', type(modified_product_data), modified_product_data)
    # print('from create_order', type(modified_product_data), 'modified_product_data=', modified_product_data)
    # crud_order.order_product.create(db=db, obj_in=jsonable_encoder(cart_row))  # order_products =
    # db_obj = self.model(**obj_in_data)  # type: ignore
    # db_obj = OrderProduct(**order_product_scheme.dict(), order_id=order_in.id)
    db_order = Order(**order_data)  # ! ! !
    db.add(db_order)
    db.commit()
    # db.refresh(db_order)
    order_id = db_order.id
    # TODO пренести создание в отдельную функцию(и) ??
    # order = crud_order.order.create(db=db, obj_in=order_in)  #  ВРЕМЕННО. УБРАТЬ ПОТОМ коммент

    # создадим запись заказа в БД для каждой записи из корзины пользователя
    # Надо перебрать все товары в корзине пользователя и добавить их в таблицу order_product
    total_cost = 0  # посчитаем общую стоимость
    total_quantity = 0  # посчитаем общее количество
    for product in cart_in:  # modified_product_data:
        # print('from create_order', type(product), 'product=', product, 'dir(product)=', dir(product))
        print('from create_order', 'product=', product, 'vars(product)=', vars(product))
        # vars(product)= {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7fcab166e5e0>,
        # 'price': 11500.0, 'id': 6, 'user_id': 1, 'quantity': 1.0, 'product_id': 2}
        product_data = vars(product)  # TODO Возможно, есть более правильный вариант преобразовать в словарь этот объект
        # например, https://coderoad.ru/61517/Python-%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D1%8C-%D0%B8%D0%B7-%D0%BF%D0%BE%D0%BB%D0%B5%D0%B9-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%B0
        # ИЛИ создание магик-методов в классе __iter__

        product_data.pop('_sa_instance_state')  # убираем поле-ключ _sa_instance_state
        product_data.pop('user_id')  # убираем поле-ключ user_id
        product_data.pop('id')  # убираем поле-ключ id
        # product_data = product.dict()  # не работает 'Cart' object has no attribute 'dict'
        # product_data = dict(product)  # TypeError: 'Cart' object is not iterable

        # print('from create_order', type(product_data), 'product=', product_data)
        # from create_order <class 'dict'> product= {'id': 6, 'price': 11500.0, 'product_id': 2, 'quantity': 1.0}

        product_data['order_id'] = order_id
        total_cost += product_data['price'] * product_data['quantity']
        total_quantity += product_data['quantity']
        # print('from create_order', type(product_data), 'product=', product_data)
        # from create_order <class 'dict'> product= {'id': 6, 'price': 11500.0, 'product_id': 2, 'quantity': 1.0, 'order_id': 51}

        db_product = OrderProduct(**product_data)  # ! ! ! id, order_id, product_id, quantity, price
        db.add(db_product)
    db_order.total_cost = total_cost
    db_order.total_quantity = total_quantity
    # db_order.order_products = cart_in  # AttributeError: 'Cart' object has no attribute '_sa_instance_state'
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    # db.refresh(db_product)
        # print('from create_order db_product=', db_product)

        # order_product = create_order_product(order_product_scheme=order_product_scheme, cart_row=cart_row, order_id=order.id, db=db)
    return db_order  # order_in   ВРЕМЕННО


@router.put("/", status_code=201, response_model=OrderSchemas, tags=["Put Methods"])
def update_order(
        *,
        order_in: OrderUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    Update order in database. Меняет статус заказа и его дату закрытия.
    """
    print('router.put update_payment', order_in.id)
    print('payment_in=', order_in)

    order = crud_order.order.get(db, id=order_in.id)
    print('order.id=', order.id)
    if not order:
        raise HTTPException(status_code=400, detail=f"Order with ID: {order_in.id} not found.")

    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"You can only update your order.")

    updated_order = crud_order.order.update(db=db, db_obj=order, obj_in=order_in)

    print('updated_payment=', updated_order)
    return updated_order


@router.delete('/delete/{order_id}/', status_code=201, response_model=OrderSchemas, tags=["Delete Methods"])
async def delete_order(
        *,
        order_in: OrderUpdateRestricted,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user),
):

    """
      Delete order from database. Удаление заказа по его id. Для владельца заказа.
    """
    order = crud_order.order.get(db, id=order_in.id)

    if not order:  # нет такого номера заказа
        raise HTTPException(status_code=403, detail=f"no such order.")

    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"You can only delete your order.")

    deleted_order = crud_order.order.remove(db=db, id=order_in.id)

    return deleted_order




# НЕ СРАБОТАЛО
# @router.post("/{order_id}/products", status_code=201, response_model=OrderProductScheme, tags=["Post Methods"])  #
# def create_order_products(
#         # *,
#         order_products: List[OrderProductCreateScheme],
#         order_id: int,
#         # current_user: User = Depends(get_current_active_user),
#         db: Session = Depends(get_db),
#         cart_in: Cart = Depends(get_cart_current_user),
# ) -> dict:
#     """
#     Create a new order_product rows in the database.
#     """
#
#     # создадим запись заказа в БД для каждой записи из корзины пользователя
#     print('from create_order', 'cart_in=', cart_in)
#     # print('from create_order', 'order_products=', order_products)
#     # if order_in.user_id != current_user.id:
#     #     raise HTTPException(status_code=403, detail=f"You can only submit order as yourself")
#     # print('order_in.id=', order_in.id)
#     # for cart_row in cart_in:
#     #     print('from create_order', type(cart_row), 'cart_row=', cart_row)
#         # crud_order.order_product.create(db=db, obj_in=jsonable_encoder(cart_row))  # order_products =
#         # db_obj = self.model(**obj_in_data)  # type: ignore
#     # db_obj = OrderProduct(**order_products, order_id=order_id)
#     db_obj = OrderProduct(jsonable_encoder(cart_in))  # NOT **cart_in.dict() NOT **cart_in , order_id=order_id
#     print('from create_order db_obj=', db_obj)
#     db.add(db_obj)
#     db.commit()
#     db.refresh(db_obj)
#     return db_obj
