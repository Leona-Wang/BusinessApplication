# Generated by Django 5.1.4 on 2024-12-19 07:34

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0010_alter_inventory_importamount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customerName', models.CharField(max_length=50, unique=True)),
                ('customerPhone', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('oneTime', 'OneTime'), ('recurring', 'Recurring')], default='oneTime', max_length=10)),
                ('orderDate', models.DateTimeField(blank=True, null=True)),
                ('mon', models.IntegerField(default=0)),
                ('tue', models.IntegerField(default=0)),
                ('wed', models.IntegerField(default=0)),
                ('thu', models.IntegerField(default=0)),
                ('fri', models.IntegerField(default=0)),
                ('createdTime', models.DateTimeField(auto_now_add=True)),
                ('updatedTime', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='functions.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderID', to='functions.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productID', to='functions.product')),
            ],
        ),
    ]