from django.shortcuts import render
from django.views import View
from .models import Skaitiklis, Saskaita

class SkaitiklisView(View):
    def get(self, request):
        skaitikliai = Skaitiklis.objects.all()
        return render(request, 'skaitikliai.html', {'skaitikliai': skaitikliai})

def saskaita_list(request):
    saskaitos = Saskaita.objects.all()
    return render(request, 'saskaita_list.html', {'saskaitos': saskaitos})