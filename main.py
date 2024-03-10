from fastapi import FastAPI, HTTPException
import uvicorn
import schema

import os
import uuid
import database
from werkzeug.security import generate_password_hash, check_password_hash

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

def user_auth(username: str, password: str) -> None | str | database.User:
    user: database.User = database.User.get_or_none(username=username)

    if not user:
        return None

    if not check_password_hash(user.password, password):
        return username
    
    user = database.User.get_or_none(username=username)
    return user

def username_reserved(username: str):
    user: database.User = database.User.get_or_none(username=username)
    if not user: 
        return False
    return True

def registration_moment(user: schema.UserRegister):
    if username_reserved(username=user.username):
        return None
    
    database.User.create(
        username=user.username,
        password=generate_password_hash(user.password, method='pbkdf2', salt_length=16),
        phone_number=user.phone_number,
        email=user.email
        )
    
    return True

@app.get('/products/{product_id}', response_model=schema.Product)
async def get_product(product_id) -> schema.Product | HTTPException:
    product: database.Product = get_product_from_db(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return product

@app.get('/products')
async def get_products(page: int = 0, limit: int = 30) -> list[schema.Product]: 
    offset: int = page*limit
    out_list = database.Product.select()
    out_list = out_list[offset:offset+limit]

    products = [
        {
            'seller': {
                'username': str(product.seller.username),
            },
            'category': {
                'name': product.category.name,
            },
            'name': str(product.name),
            'status': schema.ProductStatus(product.status),
            'price': int(product.price),
            'quantity': float(product.quantity if product.quantity else '0.0')
        }
        for product in out_list
    ]

    return products

@app.post('/users/auth')
async def get_user(user: schema.UserAuth):
    user_auth_status: str | database.User | None = user_auth(username=user.username, password=user.password)

    if not user_auth_status:
        raise HTTPException(status_code=404, detail="Invalid username")
    
    if isinstance(user_auth_status, str):
        return {'code':'400', 'detail': 'Invalid password', 'username': user_auth_status}
    
    return schema.User.model_validate(user_auth_status, from_attributes=True)

@app.post('/user/reg')
async def user_reg(user: schema.UserRegister):
    if not registration_moment(user):
        raise HTTPException(status_code=400, detail='Username is reserved')

    raise HTTPException(status_code=201, detail='Registration succes')


@app.post('/products/{product_id}')
async def update_or_create(product_id: str):

    product_to_db: database.Product = get_product_from_db(product_id=product_id)
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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)