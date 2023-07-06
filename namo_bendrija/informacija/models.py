from django.db import models

class Informacija (models.Model):
    pavadinimas = models.CharField(max_length=80, null=True)
    informacija = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Informacija"
        verbose_name_plural = 'Informacija'
        ordering = ['-date_created']
