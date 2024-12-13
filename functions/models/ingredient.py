from django.db import models
from django.core.validators import MinValueValidator
from functions.models.material import Material


# Create your models here.
class Ingredient(models.Model):
    material = models.ForeignKey("functions.Material", on_delete=models.CASCADE, related_name="ingredientMaterial")
    product = models.ForeignKey("functions.Product", on_delete=models.CASCADE, related_name="ingredientProduct")
    unit = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False)
    cost = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.material:
            print(f"MaterialPrice {self.material.unitPrice} Unit:{self.unit}")
            # 使用 self.material 直接訪問關聯的 Material 實例，避免每次都查詢資料庫
            self.cost = int(self.unit) * int(self.material.unitPrice)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # 在刪除 MaterialSource 前，刪除相關的 Material
        if self.product:
            self.product.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"""Material: {self.materialID}
Product: {self.productID}
unit: {self.unit}"""
