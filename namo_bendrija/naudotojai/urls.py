from django.urls import path
from .views import UserRegistrationView, UserLoginView, HomeView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
]