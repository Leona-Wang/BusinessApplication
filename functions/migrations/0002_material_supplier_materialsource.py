# Generated by Django 5.1.4 on 2024-12-10 05:57

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materialName', models.CharField(max_length=50, unique=True)),
                ('packAmount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('packPrice', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('unitPrice', models.IntegerField(blank=True, null=True)),
                ('lowestAmount', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplierName', models.CharField(max_length=50)),
                ('supplierPhone', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materialID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sourceMaterialID', to='functions.material')),
                ('supplierID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sourceSupplierID', to='functions.supplier')),
            ],
        ),
    ]