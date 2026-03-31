from django.db import models
from django.contrib.auth.models import User
import string
import random

# Create your models here.
class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=100.0)
    image = models.URLField()
    
    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    order_status = (
        ('Order Recieved', 'Order Recieved'),
        ('Order in Progress', 'Order in Progress'),
        ('Order Completed', 'Order Completed'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100,null=True, blank=True)
    amount = models.FloatField(default=100.0)
    status = models.CharField(max_length=100, choices=order_status, default='Order Recieved')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f'{self.order_id} Status: {self.status}'
    
    
    def generateOrderId(self,):
        res = ''.join(random.choices(string.ascii_letters, k=7))
        return res
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generateOrderId()
        super(Order, self).save(*args, **kwargs)