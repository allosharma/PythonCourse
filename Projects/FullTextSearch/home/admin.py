from django.contrib import admin
from .models import Product, CustomerDetails
from django import forms


class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerDetails
        fields = "__all__"
        widgets = {
            "address": forms.Textarea(attrs={"rows": 4, "cols": 40}),
        }


class CustomerInline(admin.TabularInline): #One another way to show the option to add is "StackedInline"
    model = CustomerDetails
    extra = 0 #Number of empty forms to add customers


# Method 1: Register the model with the admin site
# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", 
                    "description", 
                    "price",
                    "brand",
                    "category",
                    "thumbnail",
                    "status"
                    )
    exclude = ("discountPercentage", 
               "rating", 
               "stock",
               "images"
               )
    
    search_fields = ("title", 
                     "description", 
                     "price",
                     "brand",
                     "category",
                     "thumbnail"
                     )
    
    list_filter = ("brand", "category")
    
    actions = ["make_True"]

    def make_True(self, request, queryset):
        queryset.update(status=True)

    inlines = [CustomerInline]


# Method 2: Register the model with the admin site
# This method is better as it allows you to customize the admin interface
@admin.register(CustomerDetails)
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_display = ("name", 
                    "email", 
                    "phone", 
                    "address"
                    )
    
    list_filter = ("name",)
    
    readonly_fields = ("phone",)
