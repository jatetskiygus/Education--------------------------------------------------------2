from fastapi import FastAPI, HTTPException
import os
import uuid
import schema
import database
import hashlib

app = FastAPI()

salt = os.urandom(32)

class Error(Exception):
    pass

def get_product_from_db(product_id: str) -> database.Product:
    product: database.Product = database.Product.get_or_none(id=product_id)
    return product

def get_order_from_db(order_id: str) -> database.Product:
    order: database.Product = database.Product.get_or_none(id=order_id)
    return order

def get_user_from_db(user_id: str) -> database.User:
    user: database.User = database.User.get_or_none(id=user_id)
    return user

def password_to_hash(password: str) -> bytes:
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key

def user_auth(username: str, password: str) -> str | None | uuid.UUID:
    user: database.UserAuth = database.UserAuth.get_or_none(username=username)

    if not user:
        return None

    if str(password_to_hash(password=password) + salt) != user.password:
        return username

    return user

@app.get('/products/{product_id}', response_model=schema.Product)
async def get_product(product_id) -> schema.Product | HTTPException:
    product: database.Product = get_product_from_db(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return product

@app.get('/products')
async def get_products(page: int, limit: int):
    i = 0
    j = 0
    offset: int = page*limit
    out_list: list[database.Product] = []
    for product in database.Product.select().offset(offset).limit(limit):
        if i < offset:
            i+=1
            continue

        out_list.append(product)

    return out_list


@app.post('/users/auth', response_model=schema.User)
async def get_user(user: schema.UserAuth):
    user_auth_status: str | database.UserAuth | None = user_auth(username=user.eusrname, password=user.password)

    if not user_auth_status:
        raise HTTPException(status_code=404, detail="Invalid username")
    
    if isinstance(user_auth_status, str):
        return user.username
    
    return user_auth_status

@app.post('/user/reg')
async def user_reg(user: schema.UserAuth):
    """
    это функция для регистрации нового пользователя
    TODO: вынести из контроллера
    """

    # это функция для регистрации нового пользователя
    # TODO: вынести из контроллера
    user_to_db = database.UserAuth(username=user.username, password=password_to_hash(user.password), tel_number=user.tel_number, email=user.email)
    user_to_db.save()

    raise HTTPException(status_code=201, detail='Registration succes')


@app.post('/products/{product_id}')
async def update_or_create(product_id: str):

    # NOTE: фастапи сам проверяет наличие данных
    if not product_id:
        raise HTTPException(status_code=204, detail='No data')

    product_to_db: database.Product = get_product_from_db(product_id=product_id)
    # NOTE: wrong type
    # product_to_db: database.Product = product
    product_to_db.save()

    raise HTTPException(status_code=200, detail='Success')
    
@app.post('/orders/{order_id}')
async def update_order_status(new_order_status: str, order_id: str):
    order = get_order_from_db(orer_id=order_id)

    if not order: 
        raise HTTPException(status_code=404, detail="Item not found")
    
    order.status = schema.OrderStatus[new_order_status]

    raise HTTPException(status_code=201, detail='Change succes')

@app.post('/products/{product_id}')
async def update_order_status(new_product_status: str, product_id: str):
    product = get_product_from_db(product_id=product_id)

    if not product: 
        raise HTTPException(status_code=404, detail="Item not found")
    
    product.status = schema.ProductStatus[new_product_status]

    raise HTTPException(status_code=201, detail='Change succes')
