from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discountPercentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    thumbnail = models.URLField()
    images = models.JSONField(null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.title
    

class CustomerDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="customers")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name