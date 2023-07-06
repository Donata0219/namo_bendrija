from django.shortcuts import render
from .models import Informacija

def informacija_view(request):
    informacijos = Informacija.objects.all()
    context = {'informacijos': informacijos}
    return render(request, 'index.html', context)