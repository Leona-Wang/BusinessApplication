# Generated by Django 5.1.4 on 2024-12-18 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0009_material_shipday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='importAmount',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
