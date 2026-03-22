from django.db import models

# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)

    def __str__(self):
        return self.brand_name

class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    fetched_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
