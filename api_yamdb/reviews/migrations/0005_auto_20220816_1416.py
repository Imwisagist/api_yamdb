# Generated by Django 2.2.16 on 2022-08-16 11:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220813_0000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['name'], 'verbose_name': 'Жанры'},
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(3000), django.core.validators.MinValueValidator(1)]),
        ),
    ]
