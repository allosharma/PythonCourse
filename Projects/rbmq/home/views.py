from django.shortcuts import render
from home.rabbitmq import public_message
import random
from faker import Faker
    
fake = Faker('en_IN')


# Create your views here.
def index(request):
    message = f'This is a demo message {random.randint(1, 100)}'
    names = [
        {"name": fake.name(), "email": fake.email(), "address": fake.address()} for _ in range(10)
    ]
    
    public_message(names)
    return render(request, 'index.html')