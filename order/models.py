from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=255,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order{self.id} by{self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"{self.product.name} - {self.quantity} pcs"
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    added_at=models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.user.username}"



class Payment(models.Model):

    PAYMENT_METHODS=[
        ("stripe","stripe"),
        ("paypal","paypal"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, default="pending")  # Can be 'success' or 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Payment {self.transaction_id} - {self.status}"