from django.db import models
from utils.models import BaseModel
from accounts.models import Shopkeeper


class Category(BaseModel):
    name = models.CharField(max_length=255)
    comission_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
    
class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class BrandName(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products_category')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products_subcategory')
    brand = models.ForeignKey(BrandName, on_delete=models.CASCADE, related_name='products_brand')

    item_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_sku = models.CharField(max_length=100)
    hsn_code = models.CharField(max_length=20)
    maximum_retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    parent_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='variants')
    product_stock = models.PositiveIntegerField()

    def __str__(self):
        return self.item_name
    
class VariantOptions(BaseModel):
    variant_name = models.CharField(max_length=255)
    option_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.variant_name}: {self.option_name}"
    
    
class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variant')
    variant_option = models.ManyToManyField(VariantOptions, related_name='variant_option')
    # variant_name = models.CharField(max_length=255)
    # variant_sku = models.CharField(max_length=100)
    # variant_price = models.DecimalField(max_digits=10, decimal_places=2)
    # variant_stock = models.PositiveIntegerField()

    def __str__(self):
        return f"Variant of {self.product.item_name}"
    
class ProductImages(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image_url = models.URLField()

    def __str__(self):
        return f"Image for {self.product.item_name}"
    

class VendorProducts(BaseModel):
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE, related_name='vendor_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vendor_products')
    vendor_selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    dealer_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField()
    
    def get_product_details(self):
        return {
            'product_name': self.product.item_name,
            'image': self.product.product_images.first().image_url if self.product.product_images.exists() else None,
            'product_sku': self.product.product_sku,
            'hsn_code': self.product.hsn_code,
            'maximum_retail_price': self.product.maximum_retail_price,
            'category': self.product.category.name,
            'subcategory': self.product.subcategory.name,
            'brand': self.product.brand.name,
        }

    def __str__(self):
        return f"{self.shopkeeper.username} - {self.product.item_name}"
