from django.contrib import admin

# Register your models here.

from .models import Category, SubCategory, BrandName, Product, VariantOptions, ProductVariant, ProductImages, VendorProducts


class ProductAdmin(admin.ModelAdmin):
    list_display = ('item_name',
                    'category',
                    'subcategory',
                    'brand', 
                    'maximum_retail_price', 
                    'product_stock',
                    'hsn_code',
                    'product_sku',
                    'parent_product',
                    'product_description',
                    )
    search_fields = ('item_name', 'product_sku', 'hsn_code')
    list_filter = ('category', 'subcategory', 'brand', 'maximum_retail_price', 'product_stock')


class VendorProductsAdmin(admin.ModelAdmin):
    search_fields = ('product__item_name', 'product__product_sku', 'product__hsn_code')
    
class ProductVariantAdmin(admin.ModelAdmin):
    search_fields = ('product__item_name', 'variant_option__variant_name', 'variant_option__option_name')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(VendorProducts, VendorProductsAdmin)
admin.site.register(VariantOptions)
admin.site.register(ProductImages)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(BrandName)
    

