import datetime


from django.db.models.signals import post_save
from django.dispatch import receiver
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

    class Meta:

        # kad rodytų tvarkingus lietuviškus pavadinimus
        verbose_name = "Skaitiklis"
        verbose_name_plural = "Skaitikliai"
    def __str__(self):
        return f"{self.skaitiklio_vieta}  {self.iki_reiksme}"




class Savininkas (models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    phone_number = models.IntegerField()


    class Meta:
        # kad rodytų tvarkingus lietuviškus pavadinimus
        verbose_name = "Savininkas"
        verbose_name_plural = "Savininkai"

    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

class Butas (models.Model):
    buto_numeris = models.IntegerField()
    savininkas = models.OneToOneField(Savininkas, on_delete=models.SET_NULL, null=True)
    buto_plotas = models.IntegerField()
    zmoniu_skaicius = models.IntegerField()

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
    butas = models.ForeignKey(Butas, on_delete=models.SET_NULL, null=True )
    skaitiklis = models.ForeignKey(Skaitiklis, on_delete=models.SET_NULL, null=True)# ar turi buti SET_NULL, ar CASCADE?
    karsto_vandens_kiekis = models.IntegerField(verbose_name="Suvartoto karšto vandens kiekis", default=0)
    karsto_vandens_ikainis = models.FloatField(verbose_name="Karšto vandens įkainis")
    suma_karsto_vandens = models.FloatField(verbose_name="Už karštą vandenį", default=0)

    salto_vandens_kiekis = models.IntegerField(verbose_name="Suvartoto šalto vandens kiekis", default=0)
    salto_vandens_ikainis = models.FloatField(verbose_name="Šalto vandens įkainis")
    suma_salto_vandens = models.FloatField(verbose_name="Už šaltą vandenį", default=0)

    gyvatukas = models.FloatField(verbose_name="Gyvatukas", default=0)

    bendra_elektra = models.FloatField(verbose_name="Bendra elektra", default=0)

    kaupiamasis = models.FloatField(verbose_name="Kaupiamieji remontui", default=0)
    administravimo = models.FloatField(verbose_name="Administravimo mokestis", default=0)

    bendra_sildymo_suma = models.FloatField(verbose_name="Bendra suma už šildymą", default=0)
    buto_sildymas = models.FloatField(verbose_name="Šildymas", default=0)

    moketi = models.FloatField(verbose_name="Iš viso mokėti", default=0)



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

