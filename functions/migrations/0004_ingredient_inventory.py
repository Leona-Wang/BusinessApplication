# Generated by Django 5.1.4 on 2024-12-10 08:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0003_material_validday'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('materialID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientMaterialID', to='functions.material')),
                ('productID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientProductID', to='functions.product')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importPack', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('importAmount', models.IntegerField(blank=True, null=True)),
                ('importDate', models.DateField(auto_now_add=True)),
                ('expiredDate', models.DateField(blank=True, null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventoryMaterial', to='functions.material')),
            ],
        ),
    ]