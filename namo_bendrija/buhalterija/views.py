from django.http import HttpResponse, request
from django.shortcuts import render

from .models import Skaitiklis


# Create your views here.
def mokesciai (request):
    return HttpResponse ("Gyventojų mokesčiai")

def skaitiklio_parodymai (request):
    skaitiklio_vieta = request.GET.get("skaitliuko_vieta")
    iki_reiksme = request.GET.get("iki_reiksme")
    skaitiklis = Skaitiklis()
    skaitiklis.save()
    return HttpResponse(f"skaitiklio_parodymai: {skaitiklio_vieta}, {iki_reiksme} ")
