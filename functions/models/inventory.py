from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta, date


# Create your models here.
class Inventory(models.Model):
    material = models.ForeignKey("functions.Material", on_delete=models.CASCADE, related_name="inventoryMaterial")
    importPack = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False)
    importAmount = models.IntegerField(blank=False, null=False)
    importDate = models.DateField(auto_now_add=True)
    expiredDate = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.expiredDate = self.importDate + timedelta(days=self.material.validDay)
        self.importAmount = self.material.packAmount * self.importPack
        super().save(*args, **kwargs)

    def __str__(self):
        return f"""MaterialID: {self.material}
importPack: {self.importPack}
unit: {self.unit}"""
