import datetime

from _decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from naudotojai.models import MyUser


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
    updated_at = models.DateTimeField(auto_now=True)
    skirtumas = models.IntegerField()
    butas = models.ForeignKey( "Butas", on_delete=models.SET_NULL, null=True, blank=True )
    # pasirasysiu save metodas:

    def save (self, *args, **kwargs):
        if self.iki_reiksme < self.nuo_reiksme:
            raise ValueError('`Iki reikšmė` turi būti didesnė arba lygi `Nuo reikšmei`')
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

    class Meta:

        # kad rodytų tvarkingus lietuviškus pavadinimus
        verbose_name = "Skaitiklis"
        verbose_name_plural = "Skaitikliai"
    def __str__(self):
        return f"{self.skaitiklio_vieta}  {self.iki_reiksme}"




class Savininkas (models.Model):
    # first_name = models.CharField(verbose_name= "Vardas", max_length=80)
    # last_name = models.CharField(verbose_name="Pavardė", max_length=80)
    # phone_number = models.IntegerField(verbose_name="Telefono numeris")
    naudotojo_profilis = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # kad rodytų tvarkingus lietuviškus pavadinimus
        verbose_name = "Savininkas"
        verbose_name_plural = "Savininkai"

    def __str__(self):
        return f"{self.naudotojo_profilis} "

class Butas (models.Model):
    buto_numeris = models.IntegerField()
    savininkas = models.OneToOneField(Savininkas, on_delete=models.SET_NULL, null=True)
    buto_plotas = models.FloatField()
    zmoniu_skaicius = models.IntegerField()
    # created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        # kad rodytų tvarkingus lietuviškus pavadinimus
        verbose_name = "Butas"
        verbose_name_plural = "Butai"

    def __str__(self):
        return f"{self.buto_numeris}  {self.savininkas} {self.buto_plotas} {self.zmoniu_skaicius}"


class ElektrosSkaitiklis(models.Model):
    nuo_reiksme_el = models.IntegerField(verbose_name="Nuo", null=True, blank=True)
    iki_reiksme_el = models.IntegerField(verbose_name="Iki")  # įvesti skaitilnių parodymus
    created_at = models.DateTimeField(auto_now_add=True)
    skirtumas_el = models.IntegerField(verbose_name="Skirtumas")
    ikainis_el = models.FloatField()
    buto_el = models.FloatField() #mokama suma uz bendra elektros suvartojima, padalinta visiems butams
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try:
            buves_irasas_el = ElektrosSkaitiklis.objects.last()
            buvusi_iki_reiksme_el = buves_irasas_el.iki_reiksme_el
            self.nuo_reiksme_el = buvusi_iki_reiksme_el
        except AttributeError:
            pass

        self.skirtumas_el = self.iki_reiksme_el - self.nuo_reiksme_el
        self.buto_el = self.skirtumas_el * self.ikainis_el / 35

        super().save(*args, **kwargs)

    class Meta:

        # kad rodytų tvarkingus lietuviškus pavadinimus
        verbose_name = "Elektros skaitilis"
        verbose_name_plural = "Elektros skaitikliai"
    def __str__(self):
        return f"{self.buto_el}"


class Saskaita (models.Model):
    BUTO_SASKAITA_CHOICES = [
        ('sausis', 'Sausis'),
        ('vasaris', 'Vasaris'),
        ('kovas', 'Kovas'),
        ('balandis', 'Balandis'),
        ('geguze', 'Gegužė'),
        ('birzelis', 'Birželis'),
        ('liepa', 'Liepa'),
        ('rugpjutis', 'Rugpjūtis'),
        ('rugsejis', 'Rugsėjis'),
        ('spalis', 'Spalis'),
        ('lapkritis', 'Lapkritis'),
        ('gruodis', 'Gruodis'),
    ]

    butas = models.IntegerField(verbose_name="Butas", null=True )
    skaitiklis = models.ForeignKey(Skaitiklis, on_delete=models.SET_NULL, null=True)# ar turi buti SET_NULL, ar CASCADE?
    karsto_vandens_kiekis = models.IntegerField(verbose_name="Suvartoto karšto vandens kiekis", default=0)
    karsto_vandens_ikainis = models.FloatField(verbose_name="Karšto vandens įkainis")
    suma_karsto_vandens = models.DecimalField(verbose_name="Už karštą vandenį", default=Decimal('0.00'), max_digits=5, decimal_places=2)

    salto_vandens_kiekis = models.IntegerField(verbose_name="Suvartoto šalto vandens kiekis", default=0)
    salto_vandens_ikainis = models.FloatField(verbose_name="Šalto vandens įkainis")
    suma_salto_vandens = models.DecimalField(verbose_name="Už šaltą vandenį", default=Decimal('0.00'), max_digits=5, decimal_places=2)

    gyvatukas = models.FloatField(verbose_name="Gyvatukas", default=0)

    bendra_elektra = models.DecimalField(verbose_name="Bendra elektra", default=Decimal('0.00'), max_digits=5, decimal_places=2)

    kaupiamasis = models.FloatField(verbose_name="Kaupiamieji remontui", default=0)
    administravimo = models.FloatField(verbose_name="Administravimo mokestis", default=0)

    bendra_sildymo_suma = models.FloatField(verbose_name="Bendra suma už šildymą", default=0)
    buto_sildymas = models.DecimalField(verbose_name="Šildymas", default=Decimal('0.00'), max_digits=5, decimal_places=2)

    moketi = models.DecimalField(verbose_name="Iš viso mokėti", default=Decimal('0.00'), max_digits=5, decimal_places=2)

    # saskaitos_data = models.DateField(verbose_name="Sąskaitos data", null=True)
    menesis = models.CharField(verbose_name="Mėnuo", max_length=20, choices=BUTO_SASKAITA_CHOICES, null="Sausis")


    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    # šita vieta neaiški, kaip apskaičiuoti karsto vandens bendra kieki ir sudauginti jį su karšto vandens įkainiu
    def save (self, *args, **kwargs):
        # bendras karsto vandens kiekis vonioje ir virtuveje
        karsto_vandens_kiekis = 0
        skaitikliai = Skaitiklis.objects.filter(skaitiklio_vieta__in=["Karštas vonios", "Karštas virtuvės"], butas=self.butas)
        for skaitiklis in skaitikliai:
            karsto_vandens_kiekis += skaitiklis.skirtumas
        self.karsto_vandens_kiekis = karsto_vandens_kiekis
        # apskaiciuoju moketina suma uz karsta vandeni
        self.suma_karsto_vandens = self.karsto_vandens_ikainis * self.karsto_vandens_kiekis

        # Bendras salto vandens kiekis vonioje ir virtuveje
        salto_vandens_kiekis = 0
        skaitikliai = Skaitiklis.objects.filter(skaitiklio_vieta__in=["Šaltas vonios", "Šaltas virtuvės"], butas=self.butas)
        for skaitiklis in skaitikliai:
            salto_vandens_kiekis += skaitiklis.skirtumas
        self.salto_vandens_kiekis = salto_vandens_kiekis
        # apskaiciuoju moketina suma uz salta vandeni
        self.suma_salto_vandens = self.salto_vandens_ikainis * self.salto_vandens_kiekis

        # Paskaiciuoju kiek kviekvienas butas turi moketi uz bedrai sunaudota elektra
        self.bendra_elektra = ElektrosSkaitiklis.objects.last().buto_el

        self.butas = Butas.objects.last().buto_numeris

        # paskaiciuojama suma vienam butuo uz sildyma. Bendra namo sildymo sumo dalinama ir buto ploto
        self.buto_sildymas = self.bendra_sildymo_suma / Butas.objects.last().buto_plotas

        #  suskaiciuojama suma, uz visus mokescius
        self.moketi = (
                self.suma_salto_vandens +
                self.suma_karsto_vandens +
                self.gyvatukas +
                self.bendra_elektra +
                self.kaupiamasis +
                self.administravimo +
                self.buto_sildymas
        )
    #

        super().save(*args, **kwargs)

    class Meta:
        # kad rodytų tvarkingus lietuviškus pavadinimus
        verbose_name = "Sąskaita"
        verbose_name_plural = "Sąskaitos"

    def __str__(self):
        return f"{self.gyvatukas} {self.bendra_elektra} {self. karsto_vandens_ikainis} {self.salto_vandens_ikainis} {self.kaupiamasis} {self.administravimo} {self.moketi}"                f""

# bendra saskaita viso namo

