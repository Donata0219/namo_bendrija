from django.urls import path, include

from . import views
from .views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('home/', HomeView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('vartotojo_profilis/', views.vartotojo_profilis, name='vartotojo_profilis'),
]