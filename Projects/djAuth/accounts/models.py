from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.manager import UserManager


# Create your models here.

# AbstractUser model will be inherited by the CustomUser model to add additional fields to the User.
class CustomUser(AbstractUser):
    # By adding username = None, and phone_number as unique=true, we can ensure that the phone_number field is unique. And wile authenticating, we can use the phone_number field to authenticate the user.
    username = None
    phone_number = models.CharField(max_length=12, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)


    # By setting USERNAME_FIELD to phone_number, we can use the phone_number field to authenticate the user.
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()
