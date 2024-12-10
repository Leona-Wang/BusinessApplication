from django.db import models


# Create your models here.
class Supplier(models.Model):
    supplierName = models.CharField(max_length=50, blank=False, null=False, unique=False)
    supplierPhone = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return f"{self.supplierName} - {self.supplierPhone}"
