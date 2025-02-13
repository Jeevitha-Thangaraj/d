from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlist entries

    def _str_(self):
        return f"{self.user.username} - {self.product.name}"
