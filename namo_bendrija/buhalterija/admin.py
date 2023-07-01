from django.contrib import admin

# Register your models here.

from .models import Skaitiklis, Savininkas, Butas, Saskaita, ElektrosSkaitiklis


class SkaitiklisAdmin(admin.ModelAdmin):
    readonly_fields = ("skirtumas",)
    list_display = ("skaitiklio_vieta", "nuo_reiksme", "iki_reiksme", "skirtumas",)

class SaskaitaAdmin(admin.ModelAdmin):
    list_display = [
        "butas",
        "gyvatukas",
        "bendra_elektra",
        "karsto_vandens_ikainis",
        "salto_vandens_ikainis",
        "karsto_vandens_kiekis",
        "suma_karsto_vandens",
        "salto_vandens_kiekis",
        "suma_salto_vandens",
        "kaupiamasis",
        "administravimo",
        "buto_sildymas",
        "moketi",

    ]
    readonly_fields = [
        "karsto_vandens_kiekis",
        "suma_karsto_vandens",
        "salto_vandens_kiekis",
        "suma_salto_vandens",
        "bendra_elektra",
        "buto_sildymas",
        "moketi",
    ]

class ElektrosSkaitiklisAdmin(admin.ModelAdmin):
    readonly_fields = ("skirtumas_el", "buto_el")
    list_display = (
        "nuo_reiksme_el",
        "iki_reiksme_el",
        "ikainis_el",
        "skirtumas_el",
        "buto_el"
    )

class ButasAdmin (admin.ModelAdmin):
    list_display = ("buto_numeris", "buto_plotas", "zmoniu_skaicius", "savininkas")

# class SildymasAdmin (admin.ModelAdmin):
#     list_display = ("bendra_sildymo_suma",)

class SavininkasAdmin (admin.ModelAdmin):
    list_display =  ("first_name", "last_name", "phone_number", "naudotojo_profilis")

admin.site.register(Skaitiklis, SkaitiklisAdmin)
admin.site.register(Savininkas, SavininkasAdmin)
admin.site.register(Butas, ButasAdmin)
admin.site.register(Saskaita, SaskaitaAdmin)
admin.site.register(ElektrosSkaitiklis, ElektrosSkaitiklisAdmin)
# admin.site.register(Sildymas, SildymasAdmin)