# Generated by Django 4.2.2 on 2023-06-25 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buhalterija', '0004_saskaita'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elektrosskaitiklis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nuo_reiksme_el', models.IntegerField(blank=True, null=True, verbose_name='Nuo')),
                ('iki_reiksme_el', models.IntegerField(verbose_name='Iki')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('skirtumas_el', models.IntegerField(verbose_name='Skirtumas')),
                ('ikainis_el', models.FloatField()),
                ('buto_el', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='saskaita',
            name='butas',
        ),
        migrations.RemoveField(
            model_name='saskaita',
            name='skaitiklis',
        ),
    ]
