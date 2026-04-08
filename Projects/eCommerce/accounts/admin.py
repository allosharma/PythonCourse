from django.contrib import admin
from .models import Shopkeeper

# Register your models here.
class ShopkeeperAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'gst_number',)

admin.site.register(Shopkeeper, ShopkeeperAdmin)