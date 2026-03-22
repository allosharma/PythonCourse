import os
import sys
import django
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FullTextSearch.settings')

django.setup()

from home.models import Product

url = "https://dummyjson.com/products?limit=300"
response = requests.get(url)
data = response.json()

for product_data in data['products']:
    Product.objects.create(
        title=product_data['title'],
        description=product_data['description'],
        price=product_data['price'],
        discountPercentage=product_data['discountPercentage'],
        rating=product_data['rating'],
        stock=product_data['stock'],
        brand=product_data.get('brand', ''),
        category=product_data['category'],
        thumbnail=product_data['thumbnail'],
        images=",".join(product_data['images']),
        images=product_data['images'],
    )