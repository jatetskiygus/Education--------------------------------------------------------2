from pydantic import BaseModel
from enum import Enum


class ProductStatus(Enum):
    avaliable = 1
    not_avaliable = 0


class OrderStatus(Enum):
    close = 3
    arrive = 2
    delivering = 1
    collecting = 0


class User(BaseModel):
    username: str
    tel_number: str
    email: str

class UserAuth(User):
    password: str

class Category(BaseModel):
    name: str


class Product(BaseModel):
    seller: User.username
    category: Category.name 
    name: str
    status: ProductStatus
    price: int
    quantity: int | float


