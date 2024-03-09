import random
from faker import Faker
from datetime import datetime
import database
from uuid import uuid4

fake = Faker()

users = []
for _ in range(10):
    user = database.User.create(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        phone_number=fake.phone_number(),
        email=fake.email(),
        created_at=datetime.utcnow()
    )
    users.append(user)


for user in users:
    database.UserAuth.create(
        user=user,
        password=fake.password()
    )

categories = []
for _ in range(5):
    category = database.ProductCategory.create(
        name=fake.word(),
        created_at=datetime.utcnow()
    )
    categories.append(category)


products = []
for _ in range(20):
    product = database.Product.create(
        seller=random.choice(users),
        category=random.choice(categories),
        name=fake.word(),
        status=random.randint(0, 1),
        price=random.randint(10, 100),
        quantity=random.randint(1, 100)
    )
    products.append(product)


for _ in range(50):
    customer = random.choice(users)
    product = random.choice(products)
    database.OrderItem.create(
        customer=customer,
        products=product,
        status=random.randint(1, 4),
        quantity=random.randint(1, 5),
        created_at=datetime.utcnow()
    )

print("Database populated successfully!")