from django.urls import path
from .views import SkaitiklisView, saskaita_list

urlpatterns = [
    path('skaitikliai/', SkaitiklisView.as_view(), name='skaitikliai'),
    path('saskaitos/', saskaita_list, name='saskaita_list')
]