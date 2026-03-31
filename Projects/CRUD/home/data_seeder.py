import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRUD.settings')
django.setup()

from faker import Faker
from home.models import Product, Feedback


faker = Faker('en_IN')

def create_fake_products(n=10):
    for _ in range(n):
        Product.objects.create(
            name=faker.word().capitalize(),
            price=round(faker.random_number(digits=5) / 100, 2),
            description=faker.text(max_nb_chars=200)
        )

def create_fake_feedback(n=10):
    for _ in range(n):
        Feedback.objects.create(
            name=faker.name(),
            email=faker.email(),
            message=faker.text(max_nb_chars=200)
        )
        
if __name__ == '__main__':
    create_fake_products(120)  # Create 20 fake products
    create_fake_feedback(120)  # Create 20 fake feedback entries
    print("Fake data created successfully!")