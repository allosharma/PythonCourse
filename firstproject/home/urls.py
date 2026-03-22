from django.urls import path
from home.views import index, contact, dynamic_route, formPage, search_page

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('hello/<str:name>/', dynamic_route, name='dynamic_route'),
    path('form/', formPage, name='formPage'),
    path('search/', search_page, name='search_page')
]
