from django.urls import path, include

from . import views
from .views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('home/', HomeView.as_view(), name='home'),

    path('vartotojo_profilis/', views.vartotojo_profilis, name='vartotojo_profilis'),
]