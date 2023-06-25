from django.urls import path

from . import views

urlpatterns = [
    path ('', views.mokesciai, name = "pasisveikinimas"),
    path ('tax/', views.skaitiklio_parodymai, name="skaitikliu parodymai"),
]