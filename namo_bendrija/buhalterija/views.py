from django.shortcuts import render
from django.views import View
from .models import Skaitiklis, Saskaita

class SkaitiklisView(View):
    template_name = 'skaitikliai.html'
    def get(self, request):
        skaitikliai = Skaitiklis.objects.all()
        return render(request, 'skaitikliai.html', {'skaitikliai': skaitikliai})

    def post(self, request, *args, **kwargs):
        saltas_vonios = request.POST['saltas_vonios']
        saltas_virtuves = request.POST['saltas_virtuves']
        karstas_vonios = request.POST['karstas_vonios']
        karstas_virtuves = request.POST['karstas_virtuves']

        skaitiklis1 = Skaitiklis(skaitiklio_vieta=Skaitiklis.saltas_vonios, iki_reiksme=saltas_vonios)
        skaitiklis1.save()

        skaitiklis2 = Skaitiklis(skaitiklio_vieta=Skaitiklis.saltas_virtuves, iki_reiksme=saltas_virtuves)
        skaitiklis2.save()

        skaitiklis3 = Skaitiklis(skaitiklio_vieta=Skaitiklis.karstas_vonios, iki_reiksme=karstas_vonios)
        skaitiklis3.save()

        skaitiklis4 = Skaitiklis(skaitiklio_vieta=Skaitiklis.karstas_virtuves, iki_reiksme=karstas_virtuves)
        skaitiklis4.save()

        return render(request, 'skaitikliai.html', {'message': 'Duomenys išsaugoti!'})

def saskaita_list(request):
    if request.user.is_admin:
        saskaitos = Saskaita.objects.all()
    else:
        saskaitos = Saskaita.objects.filter(butas__savininkas__naudotojo_profilis=request.user)
    return render(request, 'saskaita_list.html', {'saskaitos': saskaitos})