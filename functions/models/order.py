from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta, date


# Create your models here.
class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('oneTime', 'OneTime'), # 一次性訂單
        ('recurring', 'Recurring'), # 定期訂單
    ]
    customer = models.ForeignKey("functions.Customer", on_delete=models.CASCADE, related_name="orders")
    type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default='oneTime') # 訂單類型
    orderDate = models.DateTimeField(blank=True, null=True)
    mon = models.IntegerField(default=0)
    tue = models.IntegerField(default=0)
    wed = models.IntegerField(default=0)
    thu = models.IntegerField(default=0)
    fri = models.IntegerField(default=0)

    createdTime = models.DateTimeField(auto_now_add=True) # 訂單建立時間
    updatedTime = models.DateTimeField(auto_now=True) # 訂單更新時間
    stored = models.BooleanField(default=False)

    def __str__(self):
        return f"""MaterialID: {self.material}
importPack: {self.importPack}
unit: {self.unit}"""
