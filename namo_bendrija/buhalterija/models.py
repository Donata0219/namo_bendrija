import datetime

from django.db import models

# Create your models here.
class Skaitiklis (models.Model):

    PIRMAS = "Šaltas vonios"
    ANTRAS = "Šaltas virtuvės"
    TRECIAS = "Karštas vonios"
    KETVIRTAS = "Karštas virtuvės"
    SKAITIKLIU_CHOICES =[
        (PIRMAS, 'Šaltas vonios'),
        (ANTRAS, 'Šaltas virtuvės'),
        (TRECIAS,'Karštas vonios'),
        (KETVIRTAS, 'Karštas virtuvės')
    ]
    skaitiklio_vieta = models.CharField(choices=SKAITIKLIU_CHOICES , max_length=80)
    nuo_reiksme = models.IntegerField(verbose_name="Nuo", null=True, blank=True)
    iki_reiksme = models.IntegerField(verbose_name="Iki")  #įvesti skaitilnių parodymus
    created_at = models.DateTimeField(auto_now_add=True)
    skirtumas = models.IntegerField()
    butas = models.ForeignKey( "Butas", on_delete=models.SET_NULL, null=True )
    # pasirasysiu save metodas:

    def save (self, *args, **kwargs):
    #     paiimame naujausia buvusia reiksme "iki" ir irasome i reiksme "nuo"
    # isaugoti
        try:
            buves_irasas = Skaitiklis.objects.filter(skaitiklio_vieta=self.skaitiklio_vieta, butas=self.butas).last()
            buvusi_iki_reiksme = buves_irasas.iki_reiksme
            self.nuo_reiksme = buvusi_iki_reiksme
        except AttributeError:
            pass

        self.skirtumas = self.iki_reiksme - self.nuo_reiksme

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.skaitiklio_vieta}  {self.iki_reiksme}"

class Savininkas (models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    phone_number = models.IntegerField()

    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

class Butas (models.Model):
    buto_numeris = models.IntegerField()
    savininkas = models.OneToOneField(Savininkas, on_delete=models.SET_NULL, null=True)
    buto_plotas = models.IntegerField()
    zmoniu_skaicius = models.IntegerField()

    def __str__(self):
        return f"{self.buto_numeris}  {self.savininkas} {self.buto_plotas} {self.zmoniu_skaicius}"




