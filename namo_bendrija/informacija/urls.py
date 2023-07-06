from django.urls import path
from . import views

urlpatterns = [
    path('informacija/', views.informacija_view, name='informacija'),
]