from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Ingredient(models.Model):
    material = models.ForeignKey("functions.Material", on_delete=models.CASCADE, related_name="ingredientMaterial")
    product = models.ForeignKey("functions.Product", on_delete=models.CASCADE, related_name="ingredientProduct")
    unit = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False)
    cost = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        #算個別材料的成本，之後要用可以用SUM()取
        self.cost = self.unit * self.material.unitPrice
        super().save(*args, **kwargs)

    def __str__(self):
        return f"""Material: {self.materialID}
Product: {self.productID}
unit: {self.unit}"""
