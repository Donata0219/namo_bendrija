from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, buto_numeris, password=None):
        if not email:
            raise ValueError("Vartotojas privalo turėti el. paštą")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            buto_numeris=buto_numeris,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            first_name='',
            last_name='',
            phone_number='',
            buto_numeris=0,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="El. paštas",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name="Vardas", max_length=255, null=True)
    last_name = models.CharField(verbose_name="Pavardė", max_length=255, null=True)
    phone_number = models.CharField(verbose_name="Tel. numeris", max_length=20, null=True)
    buto_numeris = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "buto_numeris"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
       return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin





