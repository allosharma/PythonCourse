import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eCommerce.settings")
django.setup()

from products.models import Product, ProductVariant, VariantOptions, ProductImages, VendorProducts
from accounts.models import Shopkeeper

import pandas as pd
from django.db import transaction
import random

VOLUME_Choice = ['250ml', '500ml', '1L', '2L']
COLOR_Choice = ['Red', 'Blue', 'Green', 'Yellow', 'Black', 'White']
WEIGHT_Choice = ['100g', '250g', '500g', '1kg', '2kg']

def generate_random_variant_options(variant):
    if variant == 'volume':
        return random.choice(VOLUME_Choice)
    elif variant == 'color':
        return random.choice(COLOR_Choice)
    elif variant == 'weight':    
        return random.choice(WEIGHT_Choice)
    else:
        return f'{variant}_option_{random.randint(1, 100)}'
    
# print(generate_random_variant_options('Alok'))

def upload_products_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        with transaction.atomic():
            for index, row in df.iterrows():
                shopkeeper = Shopkeeper.objects.get(username=row['shopkeeper_username'])
                product = Product.objects.create(
                    category_id=row['category_id'],
                    subcategory_id=row['subcategory_id'],
                    brand_id=row['brand_id'],
                    item_name=row['item_name'],
                    product_description=row['product_description'],
                    product_sku=row['product_sku'],
                    hsn_code=row['hsn_code'],
                    maximum_retail_price=row['maximum_retail_price'],
                    parent_product_id=row['parent_product_id'] if not pd.isna(row['parent_product_id']) else None,
                    product_stock=row['product_stock']
                )
                variant_option = VariantOptions.objects.create(
                    variant_name='volume',
                    option_name=generate_random_variant_options('volume')
                )
                product_variant = ProductVariant.objects.create(
                    product=product
                )
                product_variant.variant_option.add(variant_option)
                
                VendorProducts.objects.create(
                    shopkeeper=shopkeeper,
                    product=product,
                    price=row['price'],
                    stock=row['stock']
                )
    except Exception as e:
        print(f"Error uploading products: {e}")
                
        

