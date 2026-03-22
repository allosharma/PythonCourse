from django.urls import path
from tracker.views import index, deleteTransaction, registration, loginPage, logoutPage

urlpatterns = [
    path('register/', registration, name='registration'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path('', index, name='index'),
    path('delete/<uuid>', deleteTransaction, name='deleteTransaction'),
]
