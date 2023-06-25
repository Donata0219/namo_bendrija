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
    iki_reiksme = models.IntegerField(verbose_name="Iki", max_length=5)  #įvesti skaitilnių parodymus
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.skaitiklio_vieta}  {self.iki_reiksme}"

class Savininkas (models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    butas = models.IntegerField(
        Butas,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

class Butas (models.Model):
    buto_numeris = models.IntegerField(max_length=2)
    savininkas = models.ForeignKey(Savininkas, on_delete=models.SET_NULL, null=True)
    buto_plotas = models.IntegerField(max_length=3)
    zmoniu_skaicius = models.IntegerField(max_length=2)

    def __str__(self):
        return f"{self.buto_numeris}  {self.savininkas} {self.buto_plotas} {self.zmoniu_skaicius}"




