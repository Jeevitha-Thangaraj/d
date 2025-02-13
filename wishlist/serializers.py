from rest_framework import serializers
from .models import Wishlist
from store.models import Product  

class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_name', 'product_price']