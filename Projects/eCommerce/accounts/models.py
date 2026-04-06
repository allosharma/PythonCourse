from django.db import models
from django.contrib.auth.models import User
from utils.models import BaseModel

# Create your models here.
class Customer(User, BaseModel):
    profile_image = models.ImageField(upload_to='profile_images/Customer/', null=True, blank=True)
    

class Shopkeeper(User, BaseModel):
    profile_image = models.ImageField(upload_to='profile_images/Shopkeeper/', null=True, blank=True)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    aadhar_number = models.CharField(max_length=12, null=True, blank=True)
    bmp_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    vendor_name = models.CharField(max_length=255, null=True, blank=True)