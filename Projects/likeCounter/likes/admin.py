from django.contrib import admin
from likes.models import Post

# Register your models here.
# admin.site.register(Post)

# Added list of columns which will shown on the admin page.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'like']

admin.site.register(Post, PostAdmin)