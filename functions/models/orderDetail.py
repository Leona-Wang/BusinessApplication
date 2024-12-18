from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta, date


# Create your models here.
class OrderDetail(models.Model):
    order = models.ForeignKey("functions.Order", on_delete=models.CASCADE, related_name="orderID")
    product = models.ForeignKey("functions.Product", on_delete=models.CASCADE, related_name="productID")
    amount = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False)

    #def save(self, *args, **kwargs):
    #    self.updatedTime = models.DateTimeField(auto_now=True)
    #    super().save(*args, **kwargs)

    def __str__(self):
        return f"""MaterialID: {self.material}
importPack: {self.importPack}
unit: {self.unit}"""
