from django.db import models
from django.contrib.auth.models import User
import string
import random
# mporting signal to send notification in case of any change in the order status
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Create your models here.
class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=100.0)
    image = models.URLField()
    
    def __str__(self):
        return self.name


order_mapper = {
    'Order Recieved': 20,
    'Order in Progress': 40,
    'Order Completed': 60,
    'Out for Delivery': 80,
    'Delivered': 100,
}
    
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
        
    @staticmethod
    def give_order_details(order_id):
        order = Order.objects.get(order_id=order_id)
        data =  {
            'order_id': order.order_id,
            'pizza': order.pizza.name,
            'amount': order.amount,
            'status': order.status,
            'quantity': order.quantity,
            'progress_percentage': order_mapper[order.status],
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat()
        }
        return data
    
    
@receiver(post_save, sender=Order)    
def order_status_change_notification(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {
            'order_id': instance.order_id,
            'amount': instance.amount,
            'status': instance.status,
            'progress_percentage': order_mapper[instance.status],
        }
        
        async_to_sync(channel_layer.group_send)(
            f'order_{instance.order_id}',
            {
                'type': 'send_notification',
                'message': data
            }
        )