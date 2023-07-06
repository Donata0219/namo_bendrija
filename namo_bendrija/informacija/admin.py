from django.contrib import admin

from informacija.models import Informacija


# Register your models here.
class InformacijaAdmin (admin.ModelAdmin):
    list_display = ("pavadinimas","informacija", "date_created",)

admin.site.register(Informacija, InformacijaAdmin)