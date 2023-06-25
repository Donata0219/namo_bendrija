from django.contrib import admin

# Register your models here.

from .models import Skaitiklis, Savininkas, Butas, Saskaita, Elektrosskaitiklis


class SkaitiklisAdmin(admin.ModelAdmin):
    readonly_fields = ("skirtumas",)
    list_display = ("skaitiklio_vieta", "nuo_reiksme", "iki_reiksme",)

class SaskaitaAdmin(admin.ModelAdmin):
    list_display = [
        "gyvatukas",
        "bendra_elektra",
        "karsto_vandens_ikainis",
        "salto_vandens_ikainis",
        "kaupiamasis",
        "administravimo",
    ]

class ElektrosskaitiklisAdmin(admin.ModelAdmin):
    readonly_fields = ("skirtumas_el", "buto_el")
    list_display = ("nuo_reiksme_el", "iki_reiksme_el", "ikainis_el",)

class ButasAdmin (admin.ModelAdmin):
    list_display = ("buto_numeris", "buto_plotas", "zmoniu_skaicius")

admin.site.register(Skaitiklis, SkaitiklisAdmin)
admin.site.register(Savininkas)
admin.site.register(Butas, ButasAdmin)
admin.site.register(Saskaita, SaskaitaAdmin)
admin.site.register(Elektrosskaitiklis, ElektrosskaitiklisAdmin)
