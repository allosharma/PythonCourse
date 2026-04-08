from django.urls import path
from .views import registration, loginPage, logoutPage

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
]