# Generated by Django 5.1.4 on 2024-12-30 00:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0014_customer_rfmscore_customer_segment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='functions.customer'),
        ),
    ]
