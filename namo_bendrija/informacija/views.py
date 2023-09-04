from django.shortcuts import render
from .models import Informacija

def informacija_view(request):
    informacija = Informacija.objects.all()
    context = {'informacija': informacija}
    return render(request, 'index.html', context)