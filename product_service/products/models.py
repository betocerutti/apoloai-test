from django.db import models

class Product(models.Model):
    """
    Product model, represents a product in the store.

    Sensible defaults values set here to simplify Serializer implementation.
    """

    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
