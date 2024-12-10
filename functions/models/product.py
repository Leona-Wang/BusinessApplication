from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Product(models.Model):
    productName = models.CharField(max_length=50, blank=False, null=False, unique=True)
    productPrice = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False)

    def __str__(self):
        return f"{self.productName} - ${self.productPrice}"
