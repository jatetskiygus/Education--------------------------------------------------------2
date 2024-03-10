import os
import uuid
from peewee import *
import peeweedbevolve
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()

MIGRATE: bool = bool(os.environ.get('MIGRATE'))

db: PostgresqlDatabase = PostgresqlDatabase(
    os.environ.get('DB_NAME'), 
    user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'), port=os.environ.get('DB_PORT')
)

class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        database = db


class CreateUpdateMixin:
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)


class User(CreateUpdateMixin, BaseModel):
    username: str = TextField(unique=True, null=True)
    password = TextField(null=False)

    frst_name = TextField(null=True)
    last_name = TextField(null=True)

    phone_number = TextField(null=True)

    email = TextField(null=True)

    class Meta:
        db_table = 'users'


class ProductCategory(CreateUpdateMixin, BaseModel):
    name = CharField(max_length=50, null=False)

    class Meta:
        db_table = 'categories'
    

class Product(CreateUpdateMixin, BaseModel):
    seller = ForeignKeyField(model=User)
    category = ForeignKeyField(model=ProductCategory)
    
    name = CharField(max_length = 100, null=False)
    status = IntegerField(null=False)

    price = IntegerField(null=False)

    quantity = FloatField(null=True)

    class Meta:
        db_table = 'products'


class OrderItem(CreateUpdateMixin, BaseModel):
    customer = ForeignKeyField(model=User)
    products = ForeignKeyField(model=Product)

    status = IntegerField(null=False)

    quantity = FloatField(null=False)

    class Meta:
        db_table = 'orders'


if MIGRATE:
    db.evolve()