# Generated by Django 5.1.4 on 2024-12-30 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0015_alter_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stored',
            field=models.BooleanField(default=False),
        ),
    ]
