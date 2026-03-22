from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Store(models.Model):
    store_id = models.CharField(unique=True, max_length=100)
    store_name = models.CharField(max_length=100)

    def __str__(self):
        return self.store_name
