# Generated by Django 5.1.4 on 2024-12-27 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0012_alter_inventory_importdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefreshRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastRefreshDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
