from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Material(models.Model):
    materialName = models.CharField(max_length=50, blank=False, null=False, unique=True)
    #一包有幾個
    packAmount = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False)
    #一包多少錢
    packPrice = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False)
    #有效天數
    validDay = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False, default=1)
    #創建資料後自動計算packAmount/packPrice，四捨五入到整數
    shipDay = models.IntegerField(validators=[MinValueValidator(1)], blank=False, null=False, default=1)
    unitPrice = models.IntegerField(blank=True, null=True)
    #起始值設packAmount*2，之後跑模型
    lowestAmount = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # 計算單價並四捨五入
        if int(self.packAmount) > 0:
            self.packAmount = int(self.packAmount)
            self.packPrice = int(self.packPrice)
            self.validDay = int(self.validDay)
            self.unitPrice = round(self.packPrice / self.packAmount)
            self.lowestAmount = self.packAmount * 2
        super().save(*args, **kwargs)

    def __str__(self):
        return f"""Material name: {self.materialName}
Pack amount: {self.packAmount}
Pack price: {self.packPrice}
Unit price: {self.unitPrice}
Lowest amount: {self.lowestAmount}"""
