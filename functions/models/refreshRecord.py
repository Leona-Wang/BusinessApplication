from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta, date


# Create your models here.
class RefreshRecord(models.Model):
    lastRefreshDate = models.DateTimeField(auto_now_add=True)
