from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta, date


# Create your models here.
class RecurringOrder(models.Model):
    DAYS_OF_WEEK = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
    ]
    order = models.ForeignKey("functions.Order", on_delete=models.CASCADE, related_name="recurringOrder") # 顧客編號
    recurrDay = models.CharField(max_length=10, choices=DAYS_OF_WEEK, default='Mon')

    def __str__(self):
        return f"""MaterialID: {self.material}
importPack: {self.importPack}
unit: {self.unit}"""
