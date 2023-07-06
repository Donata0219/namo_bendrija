from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('naudotojai/', include('naudotojai.urls')),
    path('buhalterija/', include('buhalterija.urls')),
    path('informacija/', include('informacija.urls')),
]
