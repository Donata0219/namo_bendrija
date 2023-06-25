from django.contrib import admin

# Register your models here.

from .models import Skaitiklis, Savininkas, Butas

class SkaitiklisAdmin(admin.ModelAdmin):
    readonly_fields = ("skirtumas",)
    list_display = ("skaitiklio_vieta", "nuo_reiksme", "iki_reiksme",)

admin.site.register(Skaitiklis, SkaitiklisAdmin)
admin.site.register(Savininkas)
admin.site.register(Butas)
