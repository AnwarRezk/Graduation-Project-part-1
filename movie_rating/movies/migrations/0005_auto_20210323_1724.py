# Generated by Django 3.1.5 on 2021-03-23 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20210203_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actors_name_ar',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='actors_name_eg',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres_name_ar',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres_name_eg',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='name_ar',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='name_eg',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='movieinfo',
            name='plot',
            field=models.TextField(blank=True, null=True),
        ),
    ]
