from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta, date, datetime


# Create your models here.
class Inventory(models.Model):
    material = models.ForeignKey("functions.Material", on_delete=models.CASCADE, related_name="inventoryMaterial")
    importPack = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False)
    importAmount = models.IntegerField(blank=False, null=False)
    importDate = models.DateField(blank=False, null=False)
    expiredDate = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # 將 importDate 轉換為 datetime.date 類型（如果需要）
        if isinstance(self.importDate, str):
            self.importDate = datetime.strptime(self.importDate, "%Y-%m-%d").date()

        # 計算 expiredDate 和 importAmount
        self.expiredDate = self.importDate + timedelta(days=self.material.validDay)
        self.material.packAmount = int(self.material.packAmount)
        self.importPack = int(self.importPack)
        self.importAmount = self.material.packAmount * self.importPack

        # 調用父類的 save 方法
        super().save(*args, **kwargs)

    def __str__(self):
        return f"""MaterialID: {self.material}
importPack: {self.importPack}
unit: {self.unit}"""
