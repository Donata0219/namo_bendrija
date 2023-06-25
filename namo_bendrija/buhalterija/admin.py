from django.contrib import admin

# Register your models here.

from .models import Skaitiklis, Savininkas, Butas

admin.site.register(Skaitiklis)
admin.site.register(Savininkas)
admin.site.register(Butas)
