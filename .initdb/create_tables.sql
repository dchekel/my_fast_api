--  Вопрос, какой тип данных лучше использовать для поля id
-- В документации https://www.postgresql.org/docs/8.4/datatype-numeric.html
-- в числовых типах данных есть тип serial	4 bytes	autoincrementing integer	from 1 to 2147483647
-- или использовать integer	4 bytes	typical choice for integer	-2147483648 to +2_147_483_647
-- есть тип money	8 bytes	currency amount	-92233720368547758.08 to +92233720368547758.07
-- но мой Pycharm его не признает


-- tables

-- Table: user
create table if not exists "user" (  -- зарезервированное слово в pycharm, поэтому кавычки
  id serial,
  username varchar(100) not null,
  password varchar(200) not null,  --  какой тип данных лучше использовать для поля password ?
  first_name varchar(100),
  last_name varchar(100),
  email varchar(100) not null,
  address varchar(100) not null,
  primary key(id),
  unique(username),
  unique (email)
);

-- Table: role
create table if not exists role (
  id serial,
  name varchar(100) not null,
  primary key(id),
  unique(name)
);

-- Table: user_role
create table if not exists user_role (
  user_id integer not null,
  role_id integer not null,
  unique(user_id, role_id)
);

-- Table: payment
create table if not exists payment (
  id serial,
  amount real not null,
  paid_at timestamp,  -- также возможно TIMESTAMP WITH TIME ZONE
  order_id integer not null,
  user_id integer not null,
  primary key(id)
);

-- Table: category
create table if not exists category (
  id serial,
  name varchar(100) not null,
  primary key(id),
  unique(name)
);

-- Table: product
create table if not exists product (
  id serial,
  name varchar(100) not null,
  description text,
  price real not null ,
  category_id integer not null,
  primary key(id),
  unique(name)
);

-- Table: order
create table if not exists "order" (  -- зарезервированное слово в pycharm
  id serial,
  user_id integer not null,
  status_id integer,
  created_at timestamp,
  closed_at timestamp,
  total_cost real,
  total_quantity real, -- если у нас будет весовой или мерный товар
  primary key(id)
);

-- Table: order_product
create table if not exists order_product (
  id serial,
  order_id integer not null,
  product_id integer not null,
  quantity real,        -- если у нас будет весовой или мерный товар
  price real,
  primary key(id)
);

-- Table: order_status
create table if not exists order_status (
  id serial,
  name varchar(100) not null,
  primary key(id),
  unique(name)
);

-- Table: cart
create table if not exists cart (
  id serial,
  product_id integer not null,
  user_id integer not null,
  quantity real,          -- если у нас будет весовой или мерный товар
  price real,
  primary key(id)
);

/*
-- foreign keys
-- ALTER TABLE {table_name}   --  изменить определение таблицы (дочерней)
-- ADD CONSTRAINT {constraint_name} -- применяют для именования ограничения, чтобы потом можно было отменить его по имени:
-- FOREIGN KEY ({table_field_внешний_ключ}) -- поле в дочерней таблице, кот. является внешним ключем
-- REFERENCES Внешняя_таблица(PRIMARY_KEY_во_внешней_таблице); -- первичный ключ в родительской таблице
*/

-- Reference: user_role_user (table: user_role)
alter table user_role add constraint user_role_user
  foreign key (user_id) -- внешний ключ в таблице user_role на стороне многие
  references "user"(id);  -- первичный ключ в таблице user на стороне один

-- Reference: user_role_role (table: user_role)
alter table user_role add constraint user_role_role
  foreign key (role_id)
  references role(id); --  Если refcolumn список опущен, используется первичный ключ reftable

-- Reference: user_payment (table: payment)
alter table payment add constraint user_payment
  foreign key (user_id)
  references "user"(id);

-- Reference: user_order (table: order)
alter table "order" add constraint user_order
  foreign key (user_id)
  references "user"(id);

-- Reference: order_payment (table: payment)
alter table payment add constraint order_payment
  foreign key (order_id)
  references "order"(id);

-- Reference: order_order_status (table: order)
alter table "order" add constraint order_order_status
  foreign key (status_id)
  references order_status(id);

-- Reference: order_product_order (table: order_product)
alter table order_product add constraint order_product_order
  foreign key (order_id)
  references "order"(id);

-- Reference: order_product_product (table: order_product)
alter table order_product add constraint order_product_product
  foreign key (product_id)
  references product(id);

-- Reference: cart_product (table: cart)
alter table cart add constraint cart_product
  foreign key (product_id)
  references product(id);

-- Reference: cart_user (table: cart)
alter table cart add constraint cart_user
  foreign key (user_id)
  references "user"(id);

-- Reference: product_category (table: product)
alter table product add constraint product_category
  foreign key (category_id)
  references category(id);

-- alter table payment add column if not exists  paid_at timestamp;

/* Результат запуска
create table if not exists "user" (  -- зарезервированное слово в pycharm, поэтому кавычки
id serial,
username varchar(100) not null,
password varchar(60) not null,  --  какой тип данных лучше использовать для поля password ?
first_...
[2021-11-14 22:24:13] 0 row(s) affected in 22 ms
create table if not exists role (
id serial,
name varchar(100) not null,
primary key(id),
unique(name)
)
[2021-11-14 22:24:13] 0 row(s) affected in 1 ms
create table if not exists user_role (
user_id integer not null,
role_id integer not null,
unique(user_id, role_id)
)
[2021-11-14 22:24:13] 0 row(s) affected in 0 ms
create table if not exists payment (
id serial,
amount real not null,
order_id integer not null,
user_id integer not null,
primary key(id)
)
[2021-11-14 22:24:13] 0 row(s) affected in 88 ms
create table if not exists category (
id serial not null,
name varchar(100) not null,
primary key(id),
unique(name)
)
[2021-11-14 22:24:13] 0 row(s) affected in 1 ms
create table if not exists product (
id serial,
name varchar(100) not null,
description text,
price real not null ,
category_id integer not null,
primary key(id),
unique(name)
)
[2021-11-14 22:24:13] 0 row(s) affected in 1 ms
create table if not exists "order" (  -- зарезервированное слово в pycharm
id serial,
user_id integer not null,
status_id integer,
created_at timestamp,
closed_at timestamp,
total_cost real,
total_quantity real, -- если у нас ...
[2021-11-14 22:24:13] 0 row(s) affected in 1 ms
create table if not exists order_product (
id serial,
order_id integer not null,
product_id integer not null,
quantity real,        -- если у нас будет весовой или мерный товар
price real,
primary key(id)
)
[2021-11-14 22:24:13] 0 row(s) affected in 0 ms
create table if not exists order_status (
id serial,
name varchar(100) not null,
primary key(id),
unique(name)
)
[2021-11-14 22:24:13] 0 row(s) affected in 1 ms
create table if not exists cart (
id serial,
product_id integer not null,
user_id integer not null,
quantity real,          -- если у нас будет весовой или мерный товар
price real,
primary key(id)
)
[2021-11-14 22:24:13] 0 row(s) affected in 1 ms
alter table user_role add constraint user_role_user
foreign key (user_id) -- внешний ключ в таблице user_role на стороне многие
references "user"(id)
[2021-11-14 22:24:13] [42710] ERROR: constraint "user_role_user" for relation "user_role" already exists
alter table user_role add constraint user_role_role
foreign key (role_id)
references role(id)
[2021-11-14 22:24:13] [42710] ERROR: constraint "user_role_role" for relation "user_role" already exists
alter table payment add constraint user_payment
foreign key (user_id)
references "user"(id)
[2021-11-14 22:24:13] 0 row(s) affected in 6 ms
alter table "order" add constraint user_order
foreign key (user_id)
references "user"(id)
[2021-11-14 22:24:13] 0 row(s) affected in 2 ms
alter table payment add constraint order_payment
foreign key (order_id)
references "order"(id)
[2021-11-14 22:24:13] 0 row(s) affected in 2 ms
alter table "order" add constraint order_order_status
foreign key (status_id)
references order_status(id)
[2021-11-14 22:24:13] 0 row(s) affected in 3 ms
alter table order_product add constraint order_product_order
foreign key (order_id)
references "order"(id)
[2021-11-14 22:24:13] 0 row(s) affected in 2 ms
alter table order_product add constraint order_product_product
foreign key (product_id)
references product(id)
[2021-11-14 22:24:13] 0 row(s) affected in 3 ms
alter table cart add constraint cart_product
foreign key (product_id)
references product(id)
[2021-11-14 22:24:13] 0 row(s) affected in 2 ms
alter table cart add constraint cart_user
foreign key (user_id)
references "user"(id)
[2021-11-14 22:24:13] 0 row(s) affected in 1 ms
alter table product add constraint product_category
foreign key (category_id)
references category(id)
[2021-11-14 22:24:13] 0 row(s) affected in 1 ms
[2021-11-14 22:24:13] Summary: 21 of 21 statements executed, 2 failed in 1 s 564 ms (3104 symbols in file)
*/