# Generated by Django 3.1.5 on 2021-06-22 18:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_auto_20210404_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movieinfo',
            name='date',
        ),
        migrations.AddField(
            model_name='movie',
            name='date',
            field=models.IntegerField(default=1900, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(3000)]),
        ),
        migrations.AlterField(
            model_name='movieinfo',
            name='country',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
