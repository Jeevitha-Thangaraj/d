from django.contrib import admin
from .models import Product
from order.models import Cart,Order,OrderItem,Payment
from authentication.models import Profile
from category.models import Category









admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Profile)
admin.site.register(Category)


