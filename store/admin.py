from django.contrib import admin
from .models import Category,Product
from order.models import Cart,Order,OrderItem,Payment


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)


