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


class UserIndetifier(BaseModel):
    username: str


class User(UserIndetifier):
    phone_number: str # phone_number +7 (999) 999-99-99
    email: str

class UserAuth(UserIndetifier):
    password: str

class UserRegister(User, UserAuth):
    pass

class Category(BaseModel):
    name: str


class Product(BaseModel):
    seller: UserIndetifier
    category: Category
    name: str
    status: ProductStatus
    price: int
    quantity: int | float
