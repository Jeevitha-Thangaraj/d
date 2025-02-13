from django.db import models
from django.contrib.auth.models import User

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)

    def _str_(self):
        return f"{self.user.username} - {self.address_line_1}"

class ShippingRate(models.Model):
    country = models.CharField(max_length=100)
    standard_rate = models.DecimalField(max_digits=10, decimal_places=2)
    express_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"Rates for {self.country}"
