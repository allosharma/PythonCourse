from django.urls import path

from . import views


app_name = "compiler"

urlpatterns = [
    path("", views.home, name="home"),
    path("run/", views.run_code, name="run_code"),
]
