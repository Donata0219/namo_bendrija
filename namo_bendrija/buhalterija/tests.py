import unittest

from django.test import TestCase
from django.utils import timezone

from .models import Skaitiklis, Savininkas, Butas, ElektrosSkaitiklis, Saskaita
from naudotojai.models import MyUser



class SkaitiklisModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    # testuojama ar nuo reiksme yra mazesne uz iki reiksme
    def test_iki_reiksme_less_than_nuo_reiksme(self):
        skaitiklis = Skaitiklis(
            skaitiklio_vieta=Skaitiklis.PIRMAS, nuo_reiksme=100, iki_reiksme=50
        )
        with self.assertRaises(ValueError):
            skaitiklis.save()

    # testuojama ar skirtumas yra didesnis arba lygus nuliui
    def test_skirtumas_greater_than_or_equal_to_zero(self):
        skaitiklis = Skaitiklis(
            skaitiklio_vieta=Skaitiklis.PIRMAS, nuo_reiksme=50, iki_reiksme=100
        )
        skaitiklis.save()
        self.assertEqual(skaitiklis.skirtumas, 50)


class ElektrosSkaitiklisModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    # Elektros skaitliklio reiksmiu skirtumo skaiciavimas
    def test_skirtumas_el_skaiciavimas(self):
        elektros_skaitiklis = ElektrosSkaitiklis(
            nuo_reiksme_el=100, iki_reiksme_el=150, ikainis_el=0.5
        )
        elektros_skaitiklis.save()
        #
        # expected_skirtumas = 150 - 100
        self.assertEqual(elektros_skaitiklis.skirtumas_el, 50)

#         Elektros vienam butui paskaiciavimas
    def test_buto_el_calculation(self):
        elektros_skaitiklis = ElektrosSkaitiklis(
            nuo_reiksme_el=100, iki_reiksme_el=150, ikainis_el=0.5
        )
        elektros_skaitiklis.save()
        laukiamas_skirtumas = 150 - 100
        laukiamas_buto_el = laukiamas_skirtumas * 0.5 / 35
        self.assertAlmostEqual(elektros_skaitiklis.buto_el, laukiamas_buto_el, places=2)

#       !!!  Testuojam ar paskutinio menesio "iki" reiksme nueina i kito menesio "nuo" reiksme !!!!
#


if __name__ == '__main__':
    unittest.main()


