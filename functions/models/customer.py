from django.db import models


# Create your models here.
class Customer(models.Model):
    customerName = models.CharField(max_length=50, blank=False, null=False, unique=True)
    customerPhone = models.CharField(max_length=50, blank=False, null=False, unique=True)
    rfmScore = models.CharField(max_length=10, null=True, blank=True, default='000')
    segment = models.CharField(max_length=50, null=True, blank=True, default='未分類')

    def __str__(self):
        return f"{self.customerName} - {self.customerPhone}"
