from app.core.settings import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import String, REAL, Integer, DateTime, Text

# from sqlalchemy_utils.types import ChoiceType


# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
association_table_user_role = Table('user_role', Base.metadata,
                                    Column('user_id', ForeignKey('user.id'), primary_key=True),  # pk??
                                    Column('role_id', ForeignKey('role.id'), primary_key=True)   # pk??
                                    )


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    address = Column(String)  # , nullable=False
    # relationship
    roles = relationship("Role",
                         secondary=association_table_user_role,  # многие-ко-многим
                         back_populates="users")
    payments = relationship("Payment", back_populates="users")
    orders = relationship("Order", back_populates="users")
    carts = relationship("Cart", back_populates="users")

    def __repr__(self):
        return f"<User: {self.username}, Name: {self.first_name} {self.last_name}>"


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    # relationship
    users = relationship("User",
                         secondary=association_table_user_role,  # многие-ко-многим
                         back_populates="roles")

    def __repr__(self):
        return f"<Role: {self.name}>"


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True)
    amount = Column(REAL, nullable=False)
    paid_at = Column(DateTime)
    order_id = Column(Integer, ForeignKey('order.id'))  # nullable=False
    user_id = Column(Integer, ForeignKey('user.id'))  # nullable=False
    # relationship
    users = relationship("User", back_populates="payments")
    orders = relationship("Order", back_populates="payments")

    def __repr__(self):
        return f"<Payment(User: {self.user_id}, Sum: {self.amount}, At: {self.paid_at})>"


# В модели заказа описывается связь с таблицей товары_заказа с каскадным удалением
class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))  # nullable=False
    status_id = Column(Integer, ForeignKey('order_status.id'))  # nullable=False
    created_at = Column(DateTime)
    closed_at = Column(DateTime)
    total_cost = Column(REAL, nullable=False)
    total_quantity = Column(REAL, nullable=False)
    # relationship
    users = relationship("User", back_populates="orders")
    order_statuses = relationship("OrderStatus", back_populates="orders")
    payments = relationship("Payment", back_populates="orders")
    # order_products = relationship("OrderProduct", back_populates="orders")  # если так, тогда такое же в Order
    # А для каскадного удаления строк заказа из order_products
    # from https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete
    order_products = relationship("OrderProduct", cascade="all,delete", backref="orders")  # , back_populates="orders"

    def __repr__(self):
        return f"<Order(User: {self.user_id}, Cost: {self.total_cost})"


class OrderStatus(Base):
    __tablename__ = 'order_status'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    # relationship
    orders = relationship("Order", back_populates="order_statuses")

    def __repr__(self):
        return f"<OrderStatus: {self.name}"


class OrderProduct(Base):
    __tablename__ = 'order_product'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))  # nullable=False
    product_id = Column(Integer, ForeignKey('product.id'))  # nullable=False
    quantity = Column(REAL)
    price = Column(REAL)
    # relationship
    products = relationship("Product", back_populates="order_products")
    # orders = relationship("Order", back_populates="order_products")  # закоментил, так как  backref="orders" в Order
    # payments = relationship("Payment", back_populates="order_products")

    def __repr__(self):
        return f"<OrderProduct(Product: {self.product_id}, price: {self.price})"


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(REAL)
    category_id = Column(Integer, ForeignKey('category.id'))  # nullable=False
    # relationship
    categories = relationship("Category", back_populates="products")
    carts = relationship("Cart", back_populates="products")
    order_products = relationship("OrderProduct", back_populates="products")

    def __repr__(self):
        return f"<Product(Name: {self.name}, price: {self.price})"


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # relationship
    products = relationship("Product", back_populates="categories")

    def __repr__(self):
        return f"<Category(Name: {self.name})"


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))  # nullable=False
    user_id = Column(Integer, ForeignKey('user.id'))  # nullable=False
    quantity = Column(REAL)
    price = Column(REAL)
    # relationship
    users = relationship("User", back_populates="carts")
    products = relationship("Product", back_populates="carts")

    def __repr__(self):
        return f"<Cart(id: {self.id}, product_id: {self.product_id},user_id: {self.user_id}, quantity: {self.quantity}, price: {self.price})>"

'''
backref -
Указывает строковое имя свойства, которое должно быть помещено в класс связанного сопоставления, который будет 
обрабатывать это отношение в другом направлении. Другое свойство будет создано автоматически при настройке сопоставлений
. Также может быть передано как объект backref() для управления конфигурацией нового отношения.

back_populates -
Принимает строковое имя и имеет то же значение, что и backref, за исключением того, что дополняющее свойство 
не создается автоматически, а должно быть настроено явно на другом сопоставлении. Дополняющее свойство также должно 
указывать back_populates на это отношение для обеспечения правильного функционирования.
'''
