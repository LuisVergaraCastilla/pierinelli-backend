import math

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    height = models.FloatField()
    width = models.FloatField()
    area = models.FloatField(editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _sanitize_dimension(self, value):
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            return 0.0

        if not math.isfinite(numeric_value):
            return 0.0

        return numeric_value

    def save(self, *args, **kwargs):
        height = self._sanitize_dimension(self.height)
        width = self._sanitize_dimension(self.width)
        self.area = height * width
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
