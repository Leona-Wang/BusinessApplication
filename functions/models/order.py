from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta, date


# Create your models here.
class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('oneTime', 'OneTime'), # 一次性訂單
        ('recurring', 'Recurring'), # 定期訂單
    ]

    customer = models.ForeignKey("functions.Customer", on_delete=models.CASCADE, related_name="customer") # 顧客編號
    type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default='oneTime') # 訂單類型
    createdTime = models.DateTimeField(auto_now_add=True) # 訂單建立時間
    updatedTime = models.DateTimeField(auto_now=True) # 訂單更新時間

    def __str__(self):
        return f"""MaterialID: {self.material}
importPack: {self.importPack}
unit: {self.unit}"""
