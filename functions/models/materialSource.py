from django.db import models


# Create your models here.
class MaterialSource(models.Model):
    material = models.ForeignKey("functions.Material", on_delete=models.CASCADE, related_name="sourceMaterial")
    supplier = models.ForeignKey("functions.Supplier", on_delete=models.CASCADE, related_name="sourceSupplier")

    def __str__(self):
        return f"""MaterialID: {self.materialID}
SupplierID: {self.supplierPhone}"""
