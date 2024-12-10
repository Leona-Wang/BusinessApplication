# Generated by Django 5.1.4 on 2024-12-10 01:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=50, unique=True)),
                ('productPrice', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
    ]
