from django.contrib import admin
from .models import Product
from order.models import Order,OrderItem
from authentication.models import Profile
from category.models import Category
from wishlist.models import Wishlist
from shipping.models import ShippingAddress,ShippingRate
from review.models import Review
from cart.models import Cart






admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Wishlist)
admin.site.register(ShippingAddress)
admin.site.register(ShippingRate)
admin.site.register(Review)
admin.site.register(Cart)


